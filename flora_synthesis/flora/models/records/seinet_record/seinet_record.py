import typing

from bs4 import BeautifulSoup
from django.db import models

from flora.models.records import record
from flora.models.records.seinet_record.choices.observation_types import SEINETObservationTypeChoices
from flora.util import http_util

SESSION = http_util.get_session()


def get_placeholder_id(taxon_id: int) -> str:
    return "SEINET_PLACEHOLDER_{}".format(taxon_id)


class SEINETRecord(record.Record):
    observation_type = models.CharField(max_length=1, choices=SEINETObservationTypeChoices.choices)

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

    def load_data(self) -> typing.Optional[BeautifulSoup]:
        if self.full_metadata is not None:
            return BeautifulSoup(self.full_metadata, 'html.parser')
