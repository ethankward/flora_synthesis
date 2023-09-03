import itertools
import json
import typing

from django.db.models import Q
from django.utils import timezone
from requests_ratelimiter import LimiterSession

from flora import models
from flora.models.records.inat_record.choices.observation_types import InatObservationTypeChoices
from flora.models.taxon.choices import taxon_ranks
from flora.util import checklist_util
from flora.util import http_util

SESSION = http_util.get_session()


def get_canonical_rank(rank: str) -> typing.Optional[taxon_ranks.TaxonRankChoices]:
    return {'species': taxon_ranks.TaxonRankChoices.SPECIES,
            'hybrid': taxon_ranks.TaxonRankChoices.HYBRID,
            'variety': taxon_ranks.TaxonRankChoices.VARIETY,
            'subspecies': taxon_ranks.TaxonRankChoices.SUBSPECIES}.get(rank, None)


class InatUpdater(checklist_util.RecordUpdater):
    def get_observation_type(self) -> InatObservationTypeChoices:
        quality_grade = self.data['quality_grade']

        return {
            'research': InatObservationTypeChoices.RESEARCH,
            'needs_id': InatObservationTypeChoices.NEEDS_ID,
            'casual': InatObservationTypeChoices.CASUAL
        }.get(quality_grade, InatObservationTypeChoices.UNKNOWN)

    def get_verbatim_date(self):
        return self.data['observed_on']

    def get_date(self):
        return timezone.datetime.strptime(self.get_verbatim_date(), "%Y-%m-%d")

    def get_coordinates(self):
        if self.data['geojson'] is None:
            return None, None

        coordinates = self.data['geojson']['coordinates']
        latitude, longitude = coordinates[0], coordinates[1]
        latitude = round(latitude, 12)
        longitude = round(longitude, 12)
        return latitude, longitude

    def get_observer(self):
        return self.data['user']['login']

    def update_record(self):
        if self.data is None:
            return

        self.record.observation_type = self.get_observation_type()
        self.record.verbatim_date = self.get_verbatim_date()
        self.record.date = self.get_date()
        self.record.latitude, self.record.longitude = self.get_coordinates()
        self.record.observer = self.get_observer()

        if self.record.mapped_taxon is not None:
            mapped_taxon = self.record.mapped_taxon
            mapped_taxon.inat_id = self.record.checklist_taxon.external_id
            mapped_taxon.save()


class InatApi:
    def __init__(self, session: LimiterSession):
        self.session = session

    def read_api_data(self, url: str, parameters: dict, paginate: bool = True) -> typing.Generator[dict, None, None]:
        if not paginate:
            data = json.loads(self.session.get(url, params={**parameters}).text)
            results = data['results']
            yield from results
        else:
            for page in itertools.count(1):
                data = json.loads(self.session.get(url, params={**parameters, **{'page': page}}).text)
                results = data['results']
                if len(results) == 0:
                    break
                yield from results

    def get_urls_with_ids(self, base_url: str, ids: typing.Optional[typing.List[int]] = None):
        if ids is None:
            yield base_url
        else:
            size = 30
            for i in range(len(ids) // size + 1):
                taxon_ids_comma_delimited = ','.join(map(str, ids[size * i:size * (i + 1)]))
                url = base_url + '/' + taxon_ids_comma_delimited
                yield url

    def read_observation_data(self, parameters: dict, observation_ids: typing.Optional[typing.List[int]] = None):
        base_url = "https://api.inaturalist.org/v1/observations"
        for url in self.get_urls_with_ids(base_url, observation_ids):
            yield from self.read_api_data(url, parameters, paginate=False)

    def read_taxon_data(self, taxon_ids: typing.List[int]):
        base_url = "https://api.inaturalist.org/v1/taxa"
        for url in self.get_urls_with_ids(base_url, taxon_ids):
            yield from self.read_api_data(url, {}, paginate=False)


class InatRecordsReader(checklist_util.RecordReader):
    def read_records(self, records: typing.Optional[typing.List[models.InatRecord]] = None, limit: int = 10):
        if records is None:
            records = models.InatRecord.objects.filter(
                Q(last_refreshed__isnull=True) | Q(last_refreshed__lt=timezone.now() - timezone.timedelta(days=60)),
                checklist_taxon__checklist=self.checklist,
            ).order_by('?')

        records = records[:limit]

        records_dict = {str(record.external_id): record for record in records}
        api = InatApi(session=SESSION)

        if len(records) == 0:
            return

        observation_ids = [r.external_id for r in records]
        for observation_data_item in api.read_observation_data({}, observation_ids):
            record = records_dict[str(observation_data_item['id'])]
            record.full_metadata = json.dumps(observation_data_item)
            record.last_refreshed = timezone.now()
            record.save()


class InatChecklistReader(checklist_util.ChecklistReader):
    checklist_record_type = models.InatRecord

    def __init__(self, checklist: models.Checklist):
        super().__init__(checklist)
        self.inat_api = InatApi(session=SESSION)

    def get_family(self, ancestry: str):
        taxon_ids = list(map(int, ancestry.split('/')[::-1][1:]))
        for taxon_id in taxon_ids:
            try:
                existing = models.ChecklistTaxonFamily.objects.get(checklist=self.checklist, external_id=taxon_id)
                return existing
            except models.ChecklistTaxonFamily.DoesNotExist:
                pass

        for taxon_data_item in self.inat_api.read_taxon_data(taxon_ids):
            if taxon_data_item['rank'] == 'family':
                result = models.ChecklistTaxonFamily(checklist=self.checklist, external_id=taxon_data_item['id'],
                                                     family=taxon_data_item['name'])
                result.save()
                return result

    def update_parameters(self, new_parameters: dict):
        self.parameters = new_parameters
        self.parameters['place_id'] = self.checklist.external_checklist_id
        self.parameters['taxon_id'] = 211194
        self.parameters['per_page'] = 200

    def generate_data(self) -> typing.Generator[checklist_util.ChecklistReadItem, None, None]:
        for observation_data_item in self.inat_api.read_observation_data(self.parameters):
            ancestry = observation_data_item['taxon']['ancestry']
            taxon_name = observation_data_item['taxon']['name']
            taxon_id = observation_data_item['taxon']['id']
            record_id = observation_data_item['id']
            inat_rank = observation_data_item['taxon']['rank']

            if inat_rank in ['species', 'hybrid', 'variety', 'subspecies']:
                family = self.get_family(ancestry)
                yield checklist_util.ChecklistReadItem(
                    checklist_family=family,
                    taxon_name=taxon_name,
                    taxon_id=taxon_id,
                    record_id=record_id,
                    observation_data=observation_data_item,
                    given_rank=inat_rank,
                    canonical_rank=get_canonical_rank(inat_rank)
                )

    def load_checklist(self):
        for date_params in self.checklist.missing_dates():
            print('Updating {}'.format(date_params))
            self.update_parameters(date_params)
            self.read_all()

        self.checklist.latest_date_retrieved = timezone.now().date() - timezone.timedelta(days=2)
        self.checklist.save()
