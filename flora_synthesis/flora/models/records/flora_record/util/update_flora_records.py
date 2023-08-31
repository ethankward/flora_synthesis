from flora.models.records.flora_record.choices.observation_types import FloraObservationTypeChoices

from flora.models.records.util import record_updater
from flora.models.taxon.util import handle_taxon_name


def get_observation_type(data: dict) -> FloraObservationTypeChoices:
    if data['observation_type'] == 'True':
        return FloraObservationTypeChoices.PRESENT
    else:
        return FloraObservationTypeChoices.MISSING


class Updater(record_updater.RecordUpdater):
    def update_record(self):
        if self.data is not None:
            self.record.observation_type = get_observation_type(self.data)
            mapped_taxon_name = self.data['mapped_taxon_name']
            if mapped_taxon_name is not None:
                mapped_taxon = handle_taxon_name.TaxonName(mapped_taxon_name,
                                                           family=self.record.checklist_taxon.family.family).get_db_item()
                self.record.mapped_taxon = mapped_taxon
