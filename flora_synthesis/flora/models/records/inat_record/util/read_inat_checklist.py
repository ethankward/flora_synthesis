import typing

from flora import models
from flora.models.records.inat_record.util import inat_api
from flora.models.records.util import checklist_reader
from flora.models.taxon.choices import taxon_ranks
from flora.util import http_util

SESSION = http_util.get_session()


def get_canonical_rank(rank: str):
    if rank == 'species':
        return taxon_ranks.TaxonRankChoices.SPECIES
    elif rank == 'hybrid':
        return taxon_ranks.TaxonRankChoices.HYBRID
    elif rank == 'variety':
        return taxon_ranks.TaxonRankChoices.VARIETY
    elif rank == 'subspecies':
        return taxon_ranks.TaxonRankChoices.SUBSPECIES


class InatChecklistReader(checklist_reader.ChecklistReader):
    checklist_record_type = models.InatRecord

    def __init__(self, checklist, parameters):
        super().__init__(checklist, parameters)
        self.parameters['place_id'] = checklist.external_checklist_id
        self.parameters['taxon_id'] = 211194
        self.parameters['per_page'] = 200
        self.inat_api = inat_api.InatApi(session=SESSION)

    def get_family(self, ancestry):
        taxon_ids = ancestry.split('/')[::-1][1:]
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

    def generate_data(self) -> typing.Generator[checklist_reader.ChecklistReadItem, None, None]:
        for observation_data_item in self.inat_api.read_observation_data(self.parameters):
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
                    given_rank=inat_rank,
                    canonical_rank=get_canonical_rank(inat_rank)
                )
