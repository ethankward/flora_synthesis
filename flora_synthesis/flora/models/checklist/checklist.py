from django.db import models
from django.db.models import Q
from django.utils import timezone

from flora.models import base_model


class Checklist(base_model.BaseModel):
    class ChecklistTypeChoices(models.TextChoices):
        INAT = 'i', 'iNaturalist'
        SEINET = 's', 'SEINet'
        FLORA = 'f', 'Flora'

    checklist_name = models.TextField()
    checklist_type = models.CharField(max_length=1, choices=ChecklistTypeChoices.choices)
    checklist_state = models.CharField(max_length=32, blank=True, null=True)
    locality = models.TextField(blank=True, null=True)

    external_checklist_id = models.IntegerField(blank=True, null=True)
    local_checklist_fn = models.CharField(max_length=256, blank=True, null=True)

    latest_date_retrieved = models.DateField(blank=True, null=True)

    def __str__(self):
        return '{} ({})'.format(self.checklist_name, self.get_checklist_type_display())

    class Meta:
        unique_together = [('checklist_name',)]

    def update(self):
        from flora.util import seinet_util, inat_util, local_flora_util

        old_records = ChecklistRecord.objects.filter(Q(last_refreshed__isnull=True) | Q(
            last_refreshed__lt=timezone.now() - timezone.timedelta(
                days=60)), checklist=self, placeholder=False).order_by('?')
        print(old_records.count())
        if self.checklist_type == self.ChecklistTypeChoices.SEINET:
            ChecklistRecord.objects.filter(checklist=self).update(active=False)
            checklist_reader = seinet_util.SEINETChecklistReader(self)
            checklist_reader.read_all(reactivate=True)
            records_reader = seinet_util.SEINETRecordsReader(old_records[:5])
            records_reader.read_data()

        elif self.checklist_type == self.ChecklistTypeChoices.INAT:
            inat_util.read_full_checklist(self)

            if old_records.count() > 0:
                records_reader = inat_util.InatRecordsReader(old_records)
                records_reader.read_data()
        else:
            local_flora_util.LocalFloraReader(self).read_all()

        for record in ChecklistRecord.objects.filter(checklist=self):
            record.save()
        for checklist_taxon in ChecklistTaxon.objects.filter(checklist=self):
            checklist_taxon.save()
