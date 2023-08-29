import os
import typing

from flora import models
from flora.util import checklist_util, taxon_util


class LocalFloraReader(checklist_util.ChecklistReader):
    def __init__(self, checklist):
        super().__init__(checklist)
        self.path = os.path.join("flora", "data", "{}.txt".format(checklist.local_checklist_fn))
        self.data = open(self.path).read().split('\n')

    def generate_data(self) -> typing.Generator[checklist_util.ChecklistReadItem, None, None]:
        for row in self.data:
            external_id, checklist_taxon_name, checklist_family, obs_type, mapped_taxon_name = row.split('\t')

            data = {'observation_type': obs_type, 'mapped_taxon_name': mapped_taxon_name}
            family, _ = models.ChecklistTaxonFamily.objects.get_or_create(
                checklist=self.checklist, family=checklist_family
            )
            yield checklist_util.ChecklistReadItem(
                checklist_family=family,
                taxon_name=checklist_taxon_name,
                taxon_id=external_id,
                record_id=external_id,
                observation_data=data,
                given_rank=taxon_util.TaxonName(checklist_taxon_name).rank,
                is_placeholder=True
            )
