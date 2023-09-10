from django.db import models

from flora.models import base_model


class Record(base_model.BaseModel):
    active = models.BooleanField(default=True)
    is_placeholder = models.BooleanField(default=False)
    checklist = models.ForeignKey("checklist", on_delete=models.CASCADE)
    external_id = models.CharField(max_length=256)
    full_metadata = models.TextField(blank=True, null=True)
    last_refreshed = models.DateTimeField(blank=True, null=True)
    checklist_taxon = models.ForeignKey("ChecklistTaxon", on_delete=models.CASCADE)
    mapped_taxon = models.ForeignKey("Taxon", on_delete=models.SET_NULL, blank=True, null=True)
    notes = models.ManyToManyField("ChecklistRecordNote", blank=True)

    class Meta:
        abstract = True
        unique_together = [('checklist', 'external_id')]

    def external_url(self):
        return

    def load_data(self):
        return self.full_metadata

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.checklist_taxon.save()
