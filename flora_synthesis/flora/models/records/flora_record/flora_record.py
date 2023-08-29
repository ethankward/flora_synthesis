from django.db import models

from flora.models import record


class FloraObservationTypeChoices(models.TextChoices):
    PRESENT = 'P', 'Present'
    MISSING = 'M', 'Missing'


def get_observation_type(data):
    if data['observation_type'] == 'True':
        return FloraObservationTypeChoices.PRESENT
    else:
        return FloraObservationTypeChoices.MISSING


class FloraRecord(record.Record):
    observation_type = models.CharField(max_length=1, choices=FloraObservationTypeChoices)

    def update(self):
        data = self.get_data()
        if data is not None:
            self.observation_type = get_observation_type(data)

        super().update()
