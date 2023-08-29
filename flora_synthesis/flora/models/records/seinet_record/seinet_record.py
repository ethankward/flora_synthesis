import typing

from django.db import models

from flora.models.records import record
from flora.models.records.seinet_record.observation_types import SEINETObservationTypeChoices
from flora.models.records.seinet_record.update import Updater
from flora.util import http_util

SESSION = http_util.get_session()


def get_placeholder_id(taxon_id: int) -> str:
    return "SEINET_PLACEHOLDER_{}".format(taxon_id)


class SEINETRecord(record.Record):
    is_placeholder = models.BooleanField(default=False)
    observation_type = models.CharField(max_length=1, choices=SEINETObservationTypeChoices)

    verbatim_coordinates = models.CharField(max_length=32, blank=True, null=True)
    latitude = models.DecimalField(max_digits=32, decimal_places=12, blank=True, null=True)
    longitude = models.DecimalField(max_digits=32, decimal_places=12, blank=True, null=True)

    verbatim_date = models.CharField(max_length=32, blank=True, null=True)
    date = models.DateField(blank=True, null=True)

    verbatim_elevation = models.CharField(max_length=32, blank=True, null=True)
    elevation_ft = models.IntegerField(blank=True, null=True)

    locality = models.TextField(blank=True, null=True)
    herbarium_institution = models.TextField(blank=True, null=True)

    observer = models.TextField(blank=True, null=True)

    def external_url(self) -> typing.Optional[str]:
        if self.observation_type != SEINETObservationTypeChoices.NOTE_PLACEHOLDER:
            return "https://swbiodiversity.org/seinet/collections/individual/index.php?occid={}".format(
                self.external_id)

    def update(self):
        data = self.get_data()
        if data is not None:
            updater = Updater(data)
            self.observation_type = updater.get_observation_type()
            self.herbarium_institution = updater.get_herbarium_institution()
            self.verbatim_date = updater.get_verbatim_date()
            self.date = updater.get_date()
            self.verbatim_coordinates = updater.get_verbatim_coordinates()
            self.latitude, self.longitude = updater.get_coordinates()
            self.verbatim_elevation = updater.get_verbatim_elevation()
            self.observer = updater.get_observer()
            self.locality = updater.get_locality()
        else:
            if self.is_placeholder:
                self.observation_type = SEINETObservationTypeChoices.NOTE_PLACEHOLDER

        if self.mapped_taxon is not None:
            self.mapped_taxon.seinet_id = self.checklist_taxon.external_id

        super().update()

    def read_external_data(self):
        url = "https://swbiodiversity.org/seinet/collections/individual/index.php?occid={}".format(
            self.external_id)
        self.full_metadata = SESSION.get(url).text
        self.save()
