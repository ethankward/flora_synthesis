from django.db import models

from flora.models import base_model
from flora.models.checklist.choices import checklist_types


class Checklist(base_model.BaseModel):
    checklist_name = models.TextField()
    checklist_type = models.CharField(max_length=1, choices=checklist_types.ChecklistTypeChoices.choices)
    checklist_state = models.CharField(max_length=32, blank=True, null=True)
    locality = models.TextField(blank=True, null=True)

    external_checklist_id = models.IntegerField(blank=True, null=True)
    local_checklist_fn = models.CharField(max_length=256, blank=True, null=True)

    latest_date_retrieved = models.DateField(blank=True, null=True)

    earliest_year = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return '{} ({})'.format(self.checklist_name, self.get_checklist_type_display())

    class Meta:
        unique_together = [('checklist_name',)]
