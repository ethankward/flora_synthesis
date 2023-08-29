import json
import os
import typing

from flora import models
from flora.util import checklist_util, taxon_util



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
