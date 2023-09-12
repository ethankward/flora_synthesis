import typing

from bs4 import BeautifulSoup
from django.db.models import Q
from django.utils import timezone

from flora import models
from flora.models.records.seinet_record.choices.observation_types import SEINETObservationTypeChoices
from flora.models.taxon.choices import taxon_ranks
from flora.util import checklist_util, taxon_name_util, http_util

SESSION = http_util.get_session()


def get_canonical_rank(name: str) -> typing.Optional[taxon_ranks.TaxonRankChoices]:
    try:
        return taxon_name_util.TaxonName(name).rank
    except ValueError:
        return None


def parse_seinet_date(date_str: str) -> typing.Optional[timezone.datetime]:
    if date_str in ['s.d.', 'unknown']:
        return None

    date_formats = ["%Y-%m-%d"]

    for date_format in date_formats:
        try:
            return timezone.datetime.strptime(date_str, date_format)
        except ValueError:
            pass


class SEINetUpdater(checklist_util.RecordUpdater):
    def get_div_value_if_present(self, div_id: str, func: typing.Callable[[str], typing.Any]) -> typing.Optional[str]:
        try:
            text = self.data.find('div', attrs={'id': div_id}).text
        except AttributeError:
            return
        return func(text.replace('\t', '').replace('\xa0', ' ').strip())

    def get_title(self) -> str:
        return self.data.find('div', attrs={'class': 'title1-div'}).text.strip()

    def is_general_research_observation(self) -> bool:
        return 'General Research Observations' in self.get_title()

    def is_collection(self) -> bool:
        return not self.is_general_research_observation()

    def get_observation_type(self) -> SEINETObservationTypeChoices:
        if self.is_general_research_observation():
            return SEINETObservationTypeChoices.GENERAL_RESEARCH
        else:
            return SEINETObservationTypeChoices.COLLECTION

    def get_herbarium_institution(self) -> typing.Optional[str]:
        if self.is_collection():
            return self.get_title()

    def get_verbatim_date(self) -> str:
        return self.get_div_value_if_present('verbeventid-div', lambda t: t.split(': ')[1])

    def get_date(self) -> str:
        return self.get_div_value_if_present('eventdate-div', lambda t: parse_seinet_date(t.split(': ')[1]))

    def get_verbatim_coordinates(self) -> str:
        return self.get_div_value_if_present('latlngdiv', lambda t: t)

    def get_coordinates(self) -> typing.Tuple[typing.Optional[float], typing.Optional[float]]:
        verbatim_coordinates = self.get_verbatim_coordinates()
        if verbatim_coordinates is not None:
            latitude = float(verbatim_coordinates.split(' ')[0])
            longitude = float(verbatim_coordinates.split(' ')[2])
            return latitude, longitude
        return None, None

    def get_verbatim_elevation(self) -> str:
        return self.get_div_value_if_present('elev-div', lambda t: t.split('\n')[-1])

    def get_observer(self) -> str:
        return self.get_div_value_if_present('recordedby-div', lambda t: t.split('\n')[1])

    def get_locality(self) -> str:
        return self.get_div_value_if_present('locality-div', lambda t: t.split('Locality: ')[1])

    def get_type_status(self) -> str:
        return self.get_div_value_if_present('typestatus-div', lambda t: t.split('Type Status: ')[1])

    def update_record(self):
        if self.data is not None:
            self.record.observation_type = self.get_observation_type()
            self.record.herbarium_institution = self.get_herbarium_institution()
            self.record.verbatim_date = self.get_verbatim_date()
            self.record.date = self.get_date()
            self.record.verbatim_coordinates = self.get_verbatim_coordinates()
            self.record.latitude, self.record.longitude = self.get_coordinates()
            self.record.verbatim_elevation = self.get_verbatim_elevation()
            self.record.observer = self.get_observer()
            self.record.locality = self.get_locality()
            self.record.type_status = self.get_type_status()
        else:
            if self.record.is_placeholder:
                self.record.observation_type = SEINETObservationTypeChoices.NOTE_PLACEHOLDER

        if self.record.mapped_taxon is not None:
            mapped_taxon = self.record.mapped_taxon
            mapped_taxon.seinet_id = self.record.checklist_taxon.external_id
            mapped_taxon.save()


class SEINETRecordReader(checklist_util.RecordReader):
    def read_records(self, records: typing.Optional[typing.List[models.SEINETRecord]] = None, limit: int = 10):
        if records is None:
            records = models.SEINETRecord.objects.filter(
                Q(last_refreshed__isnull=True) | Q(last_refreshed__lt=timezone.now() - timezone.timedelta(days=60)),
                checklist_taxon__checklist=self.checklist,
                is_placeholder=False
            ).order_by('?')

        for record in records[:limit]:
            url = "https://swbiodiversity.org/seinet/collections/individual/index.php?occid={}".format(
                record.external_id)
            record.full_metadata = SESSION.get(url).text
            record.last_refreshed = timezone.now()
            record.save()


class SEINETChecklistReader(checklist_util.ChecklistReader):
    checklist_record_type = models.SEINETRecord

    def __init__(self, checklist: models.Checklist):
        super().__init__(checklist)
        self.seinet_checklist_id = checklist.external_checklist_id
        self.base_url = "https://swbiodiversity.org/seinet/checklists/checklist.php?clid=%s"%self.seinet_checklist_id

    def get_soup(self, page: int):
        return BeautifulSoup(SESSION.get(self.base_url, params={'pagenumber': page}).text, 'html.parser')

    def total_pages(self) -> typing.Optional[int]:
        soup = self.get_soup(1)

        for div in soup.find_all('div', {'class': 'printoff'}):
            if 'Page 1 of ' in div.text:
                return int(div.text.split('1 of ')[1].split(':')[0])

    def generate_data(self, page=None) -> typing.Generator[checklist_util.ChecklistReadItem, None, None]:
        total_pages = self.total_pages()
        if total_pages is None:
            return
        family = None

        if page is None:
            pages = range(1, total_pages + 1)
        else:
            pages = [page]

        for page in pages:
            soup = self.get_soup(page)

            taxalist_div = soup.find('div', attrs={'id': 'taxalist-div'})

            for div in taxalist_div.find_all('div'):
                classes = div.get('class', [])
                if 'family-div' in classes:
                    family_name = div.text.strip().title()
                    family, _ = models.ChecklistTaxonFamily.objects.get_or_create(
                        checklist=self.checklist, family=family_name
                    )

                if 'taxon-container' in classes:
                    taxon_name = div.find('span', attrs={'class': 'taxon-span'}).text
                    notes_div = div.find('div', attrs={'class': 'note-div'})
                    taxon_id = int(div.get('id').split('-')[1])
                    count = 0
                    canonical_rank = get_canonical_rank(
                        taxon_name)
                    if canonical_rank is not None:
                        if notes_div is not None:
                            for record_a in notes_div.find_all('a'):
                                record_id = int(record_a.get('onclick').split('(')[1].split(')')[0])
                                record_css_id = record_a.get('id', '')

                                if not record_css_id.startswith('lessvouch') and not record_css_id.startswith(
                                        'morevouch'):
                                    yield checklist_util.ChecklistReadItem(
                                        checklist_family=family,
                                        taxon_name=taxon_name,
                                        taxon_id=str(taxon_id),
                                        record_id=str(record_id),
                                        observation_data=None,
                                        given_rank=canonical_rank.name.lower(),
                                        canonical_rank=canonical_rank
                                    )
                                    count += 1
                        if count == 0:
                            yield checklist_util.ChecklistReadItem(checklist_family=family,
                                                                   taxon_name=taxon_name,
                                                                   taxon_id=str(taxon_id),
                                                                   record_id="placeholder_{}_{}".format(taxon_name,
                                                                                                        taxon_id),
                                                                   observation_data=None,
                                                                   given_rank=canonical_rank.name.lower(),
                                                                   is_placeholder=True,
                                                                   canonical_rank=canonical_rank)

    def load_checklist(self, page=None):
        models.SEINETRecord.objects.filter(checklist_taxon__checklist=self.checklist).update(active=False)
        self.read_all(reactivate=True, page=page)

        self.checklist.latest_date_retrieved = timezone.now().date()
        self.checklist.save()
