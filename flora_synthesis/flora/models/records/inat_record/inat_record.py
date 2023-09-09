import json
import typing

from django.db import models

from flora.models.records import record
from flora.models.records.inat_record.choices.observation_types import InatObservationTypeChoices


class InatRecord(record.Record):
    observation_type = models.CharField(max_length=1, choices=InatObservationTypeChoices.choices)

    latitude = models.DecimalField(max_digits=32, decimal_places=12, blank=True, null=True)
    longitude = models.DecimalField(max_digits=32, decimal_places=12, blank=True, null=True)

    date = models.DateField(blank=True, null=True)
    observer = models.TextField(blank=True, null=True)

    def external_url(self) -> str:
        return "https://www.inaturalist.org/observations/{}".format(self.external_id)

    def load_data(self) -> typing.Optional[dict]:
        if self.full_metadata is not None:
            return json.loads(self.full_metadata)

    def save(self, *args, **kwargs):
        from flora.util import inat_util
        inat_util.InatUpdater(self).update_record()

        if self.observation_type == InatObservationTypeChoices.CASUAL:
            self.active = False

        super().save(*args, **kwargs)
