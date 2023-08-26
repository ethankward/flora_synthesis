import json
import os

from flora import models
from flora.util import checklist_util, taxon_util


class LocalFloraReader(checklist_util.ChecklistReader):
    def __init__(self, checklist):
        super().__init__(checklist)
        self.path = os.path.join("flora", "data", "{}.txt".format(checklist.local_checklist_fn))
        self.data = open(self.path).read().split('\n')

    def generate_data(self):
        for row in self.data:
            external_id, checklist_taxon_name, checklist_family, obs_type, mapped_taxon_name = row.split('\t')
            if len(checklist_taxon_name.split(' ')) < 6:
                data = {'observation_type': obs_type, 'mapped_taxon_name': mapped_taxon_name}
                print(checklist_family, checklist_taxon_name)
                family, _ = models.ChecklistFamily.objects.get_or_create(
                    checklist=self.checklist, family=checklist_family
                )
                yield family, checklist_taxon_name, external_id, external_id, data, taxon_util.TaxonName(
                    checklist_taxon_name).rank


class LocalFloraUpdater(checklist_util.IndividualRecordUpdater):
    def __init__(self, checklist_record):
        super().__init__(checklist_record)
        if checklist_record.full_metadata is not None:
            self.data = json.loads(checklist_record.full_metadata)
        else:
            self.data = None

    def get_canonical_rank(self, name, rank):
        try:
            return taxon_util.TaxonName(name).rank
        except ValueError:
            return

    def get_observation_type(self):
        if self.data['observation_type'] == 'True':
            observation_type = models.ObservationTypeChoices.BOWERS_PRESENT
        else:
            observation_type = models.ObservationTypeChoices.BOWERS_MISSING
        return models.ObservationType.objects.get(observation_type=observation_type)

    def get_mapped_taxon(self, name, family, rank):
        tn = self.data['mapped_taxon_name']
        if tn != 'None':
            return taxon_util.TaxonName(tn, family=family).get_db_item()
