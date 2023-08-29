import itertools
import json
import typing

from flora import models
from flora.models.checklist.readers import checklist_reader
from flora.util import http_util

SESSION = http_util.get_session()


def read_api_data(url, parameters, paginate=True):
    print(url, parameters)
    if not paginate:
        data = json.loads(SESSION.get(url, params={**parameters}).text)
        results = data['results']
        yield from results
    else:
        for page in itertools.count(1):
            data = json.loads(SESSION.get(url, params={**parameters, **{'page': page}}).text)
            results = data['results']
            if len(results) == 0:
                break
            yield from results


def get_urls_with_ids(base_url, ids=None):
    if ids is None:
        yield base_url
    else:
        size = 30

        for i in range(len(ids)//size + 1):
            taxon_ids_comma_delimited = ','.join(map(str, ids[size*i:size*(i + 1)]))
            url = base_url + '/' + taxon_ids_comma_delimited
            yield url


def read_taxon_data(taxon_ids):
    base_url = "https://api.inaturalist.org/v1/taxa"
    for url in get_urls_with_ids(base_url, taxon_ids):
        yield from read_api_data(url, {}, paginate=False)


def read_observation_data(parameters, observation_ids=None):
    base_url = "https://api.inaturalist.org/v1/observations"
    for url in get_urls_with_ids(base_url, observation_ids):
        yield from read_api_data(url, parameters)


class InatChecklistReader(checklist_reader.ChecklistReader):
    def __init__(self, checklist, parameters):
        super().__init__(checklist, parameters)
        self.parameters['place_id'] = checklist.external_checklist_id
        self.parameters['taxon_id'] = 211194
        self.parameters['per_page'] = 200

    def get_family(self, ancestry):
        taxon_ids = ancestry.split('/')[::-1][1:]
        for taxon_id in taxon_ids:
            try:
                existing = models.ChecklistTaxonFamily.objects.get(checklist=self.checklist, external_id=taxon_id)
                return existing
            except models.ChecklistTaxonFamily.DoesNotExist:
                pass

        for taxon_data_item in read_taxon_data(taxon_ids):
            if taxon_data_item['rank'] == 'family':
                result = models.ChecklistTaxonFamily(checklist=self.checklist, external_id=taxon_data_item['id'],
                                                     family=taxon_data_item['name'])
                result.save()
                return result

    def generate_data(self) -> typing.Generator[checklist_reader.ChecklistReadItem, None, None]:
        for observation_data_item in read_observation_data(self.parameters):
            ancestry = observation_data_item['taxon']['ancestry']
            taxon_name = observation_data_item['taxon']['name']
            taxon_id = observation_data_item['taxon']['id']
            record_id = observation_data_item['id']
            inat_rank = observation_data_item['taxon']['rank']

            if inat_rank in ['species', 'hybrid', 'variety', 'subspecies']:
                family = self.get_family(ancestry)
                yield checklist_reader.ChecklistReadItem(
                    checklist_family=family,
                    taxon_name=taxon_name,
                    taxon_id=taxon_id,
                    record_id=record_id,
                    observation_data=observation_data_item,
                    given_rank=inat_rank
                )
            else:
                continue
