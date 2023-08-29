from django.db import models

from flora.models.records import record


class InatRecord(record.Record):
    class InatObservationTypeChoices(models.TextChoices):
        RESEARCH = 'R', 'Research grade'
        NEEDS_ID = 'N', 'Needs ID'
        CASUAL = 'C', 'Casual'

    observation_type = models.CharField(max_length=1, choices=InatObservationTypeChoices)

    latitude = models.DecimalField(max_digits=32, decimal_places=12, blank=True, null=True)
    longitude = models.DecimalField(max_digits=32, decimal_places=12, blank=True, null=True)

    date = models.DateField(blank=True, null=True)
    observer = models.TextField(blank=True, null=True)

    def external_url(self):
        return "https://www.inaturalist.org/observations/{}".format(self.external_id)

    def update(self):
        super().update()

        if self.mapped_taxon is not None:
            self.mapped_taxon.inat_id = self.checklist_taxon.external_id
