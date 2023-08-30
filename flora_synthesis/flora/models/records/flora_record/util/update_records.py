from models.records.flora_record.choices.observation_types import FloraObservationTypeChoices

from models.records.util import record_updater


def get_observation_type(data: dict) -> FloraObservationTypeChoices:
    if data['observation_type'] == 'True':
        return FloraObservationTypeChoices.PRESENT
    else:
        return FloraObservationTypeChoices.MISSING


class Updater(record_updater.RecordUpdater):
    def update_record(self):
        if self.data is not None:
            self.record.observation_type = get_observation_type(self.data)
