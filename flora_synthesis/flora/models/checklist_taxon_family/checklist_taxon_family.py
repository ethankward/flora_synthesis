from django.db import models

from flora.models import base_model


class ChecklistTaxonFamily(base_model.BaseModel):
    family = models.CharField(max_length=256)
    checklist = models.ForeignKey("Checklist", on_delete=models.CASCADE)
    external_id = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        unique_together = [('checklist', 'family'), ('checklist', 'external_id')]
        indexes = [models.Index(fields=['family', 'checklist'])]

    def __str__(self):
        return '{}'.format(self.family)
