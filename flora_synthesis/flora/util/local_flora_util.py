import os
import typing

from flora import models
from flora.models.records.flora_record.choices.observation_types import FloraObservationTypeChoices
from flora.models.taxon.choices import taxon_ranks
from flora.util import checklist_util, taxon_name_util


def get_canonical_rank(name: str) -> taxon_ranks.TaxonRankChoices:
    return taxon_name_util.TaxonName(name).rank


class LocalFloraUpdater(checklist_util.RecordUpdater):
    def get_observation_type(self) -> FloraObservationTypeChoices:
        if self.data['observation_type'] == 'True':
            return FloraObservationTypeChoices.PRESENT
        else:
            return FloraObservationTypeChoices.MISSING

    def update_record(self):
        if self.data is not None:
            self.record.observation_type = self.get_observation_type()
            mapped_taxon_name = self.data['mapped_taxon_name']

            if mapped_taxon_name != 'None' and self.record.mapped_taxon is None:
                mapped_taxon = taxon_name_util.TaxonName(mapped_taxon_name,
                                                         family=self.record.checklist_taxon.family.family).get_db_item()

                self.record.mapped_taxon = mapped_taxon


class LocalFloraReader(checklist_util.ChecklistReader):
    checklist_record_type = models.FloraRecord

    def __init__(self, checklist: models.Checklist):
        super().__init__(checklist)
        self.path = os.path.join("flora", "data", "{}.txt".format(checklist.local_checklist_fn))
        self.data = open(self.path).read().split('\n')

    def generate_data(self) -> typing.Generator[checklist_util.ChecklistReadItem, None, None]:
        for row in self.data:
            external_id, checklist_taxon_name, checklist_family, obs_type, mapped_taxon_name = row.split('\t')
            if mapped_taxon_name == 'None':
                mapped_taxon_name = None
            data = {'observation_type': obs_type, 'mapped_taxon_name': mapped_taxon_name}
            family, _ = models.ChecklistTaxonFamily.objects.get_or_create(
                checklist=self.checklist, family=checklist_family
            )
            canonical_rank = get_canonical_rank(checklist_taxon_name)
            yield checklist_util.ChecklistReadItem(
                checklist_family=family,
                taxon_name=checklist_taxon_name,
                taxon_id=external_id,
                record_id=external_id,
                observation_data=data,
                given_rank=canonical_rank.name,
                canonical_rank=canonical_rank,
                is_placeholder=True
            )

    def load_checklist(self):
        self.read_all()
