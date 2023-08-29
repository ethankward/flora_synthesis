import typing

from bs4 import BeautifulSoup
from django.utils import timezone

from flora import models
from flora.util import http_util, checklist_util, taxon_util

SESSION = http_util.get_session()


def get_canonical_rank(name):
    try:
        return taxon_util.TaxonName(name).rank
    except ValueError:
        return


class SEINETChecklistReader(checklist_util.ChecklistReader):
    def __init__(self, checklist):
        super().__init__(checklist)
        self.seinet_checklist_id = checklist.external_checklist_id
        self.base_url = "https://swbiodiversity.org/seinet/checklists/checklist.php?clid=%s"%self.seinet_checklist_id

    def get_soup(self, page):
        return BeautifulSoup(SESSION.get(self.base_url, params={'pagenumber': page}).text, 'html.parser')

    def total_pages(self):
        soup = self.get_soup(1)

        for div in soup.find_all('div', {'class': 'printoff'}):
            if 'Page 1 of ' in div.text:
                return int(div.text.split('1 of ')[1].split(':')[0])

    def generate_data(self) -> typing.Generator[checklist_util.ChecklistReadItem, None, None]:
        total_pages = self.total_pages()
        if total_pages is None:
            return
        family_name = None
        family = None

        for page in range(1, total_pages + 1):
            soup = self.get_soup(page)

            taxalist_div = soup.find('div', attrs={'id': 'taxalist-div'})

            for div in taxalist_div.find_all('div'):
                classes = div.get('class', [])
                if 'family-div' in classes:
                    family_name = div.text.strip().title()
                    family, _ = models.ChecklistFamily.objects.get_or_create(
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
                                        given_rank=canonical_rank.name.lower()
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
                                                                   is_placeholder=True)


def parse_seinet_date(date_str: str):
    if date_str in ['s.d.', 'unknown']:
        return

    date_formats = ["%Y-%m-%d"]

    for date_format in date_formats:
        try:
            return timezone.datetime.strptime(date_str, date_format)
        except ValueError:
            pass


class SEINETRecordsReader(checklist_util.RecordsReader):
    def read_data(self):
        for record in self.checklist_records:
            print(record)
            url = "https://swbiodiversity.org/seinet/collections/individual/index.php?occid={}".format(
                record.external_record_id)
            record.full_metadata = SESSION.get(url).text
            record.save()


class SEINETRecordUpdater(checklist_util.IndividualRecordUpdater):
    def __init__(self, checklist_record):
        super().__init__(checklist_record)
        data = checklist_record.full_metadata
        if data is not None:
            self.soup = BeautifulSoup(data, 'html.parser')
        else:
            self.soup = None

    def get_div_value_if_present(self, div_id, func):
        try:
            text = self.soup.find('div', attrs={'id': div_id}).text
        except AttributeError:
            return
        return func(text.replace('\t', '').replace('\xa0', ' ').strip())

    def get_title(self):
        return self.soup.find('div', attrs={'class': 'title1-div'}).text.strip()

    def is_general_research_observation(self):
        return 'General Research Observations' in self.get_title()

    def is_collection(self):
        return not self.is_general_research_observation()

    def get_observation_type(self):
        if self.is_general_research_observation():
            observation_type = models.ObservationTypeChoices.SEINET_GENERAL_RESEARCH
        else:
            observation_type = models.ObservationTypeChoices.SEINET_COLLECTION
        return models.ObservationType.objects.get(observation_type=observation_type)

    def get_herbarium_institution(self):
        if self.is_collection():
            return self.get_title()

    def get_verbatim_date(self):
        return self.get_div_value_if_present('verbeventid-div', lambda t: t.split(': ')[1])

    def get_date(self):
        return self.get_div_value_if_present('eventdate-div', lambda t: parse_seinet_date(t.split(': ')[1]))

    def get_verbatim_coordinates(self):
        return self.get_div_value_if_present('latlngdiv', lambda t: t)

    def get_coordinates(self):
        verbatim_coordinates = self.get_verbatim_coordinates()
        if verbatim_coordinates is not None:
            latitude = float(verbatim_coordinates.split(' ')[0])
            longitude = float(verbatim_coordinates.split(' ')[2])
            return latitude, longitude
        return None, None

    def get_verbatim_elevation(self):
        return self.get_div_value_if_present('elev-div', lambda t: t.split('\n')[-1])

    def get_observer(self):
        return self.get_div_value_if_present('recordedby-div', lambda t: t.split('\n')[1])

    def get_locality(self):
        return self.get_div_value_if_present('locality-div', lambda t: t.split('Locality: ')[1])

    def get_canonical_rank(self, name, rank):
        return get_canonical_rank(name)
