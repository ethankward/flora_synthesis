import json

from django.db import models
from django.utils import timezone

from flora.models import base_model


class Record(base_model.BaseModel):
    active = models.BooleanField(default=True)
    external_id = models.CharField(max_length=256)
    full_metadata = models.TextField(blank=True, null=True)
    last_refreshed = models.DateTimeField(blank=True, null=True)
    checklist_taxon = models.ForeignKey("ChecklistTaxon", on_delete=models.CASCADE)
    mapped_taxon = models.ForeignKey("Taxon", on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        abstract = True
        unique_together = [('external_id',)]

    def external_url(self):
        return

    def get_data(self):
        if self.full_metadata is not None:
            return json.loads(self.full_metadata)

    def update(self):
        from flora.util import taxon_util

        if self.pk is None:
            return

        if self.mapped_taxon is None:
            checklist_taxon = self.checklist_taxon
            mapped_taxon = taxon_util.TaxonName(checklist_taxon.taxon_name,
                                                family=checklist_taxon.family.family).get_db_item()
            self.mapped_taxon = mapped_taxon

        self.last_refreshed = timezone.now()

    def read_external_data(self):
        pass
