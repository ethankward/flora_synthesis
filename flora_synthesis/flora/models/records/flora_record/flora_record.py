import json
import typing

from django.db import models

from flora.models.records import record
from flora.models.records.flora_record.choices.observation_types import FloraObservationTypeChoices


class FloraRecord(record.Record):
    observation_type = models.CharField(max_length=1, choices=FloraObservationTypeChoices.choices)

    def load_data(self) -> typing.Optional[dict]:
        if self.full_metadata is not None:
            return json.loads(self.full_metadata)

    def save(self, *args, **kwargs):
        from flora.util import local_flora_util

        local_flora_util.LocalFloraUpdater(self).update_record()
        super().save(*args, **kwargs)
