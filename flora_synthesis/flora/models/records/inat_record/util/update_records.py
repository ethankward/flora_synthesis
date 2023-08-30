from django.utils import timezone

from models.records.util import record_updater
from models.records.inat_record.choices.observation_types import InatObservationTypeChoices


class Updater(record_updater.RecordUpdater):
    def get_observation_type(self) -> InatObservationTypeChoices:
        quality_grade = self.data['quality_grade']

        if quality_grade == 'research':
            observation_type = InatObservationTypeChoices.RESEARCH
        elif quality_grade == 'needs_id':
            observation_type = InatObservationTypeChoices.NEEDS_ID
        elif quality_grade == 'casual':
            observation_type = InatObservationTypeChoices.CASUAL
        else:
            observation_type = InatObservationTypeChoices.UNKNOWN

        return observation_type

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
