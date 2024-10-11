from django.db import models
from django.db.models import Q
from django.utils import timezone

from flora.models import base_model
from flora.models.checklist.choices import checklist_types
from flora.util import date_util


class Checklist(base_model.BaseModel):
    checklist_name = models.TextField()
    checklist_type = models.CharField(
        max_length=1, choices=checklist_types.ChecklistTypeChoices.choices
    )
    checklist_state = models.CharField(max_length=32, blank=True, null=True)
    locality = models.TextField(blank=True, null=True)

    external_checklist_id = models.IntegerField(blank=True, null=True)
    local_checklist_fn = models.CharField(max_length=256, blank=True, null=True)

    latest_date_retrieved = models.DateField(blank=True, null=True)

    earliest_year: int = models.IntegerField(blank=True, null=True)

    primary_checklist = models.BooleanField(default=False)

    collector_name = models.CharField(max_length=256, blank=True, null=True)

    citation = models.TextField(blank=True, null=True)
    citation_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return "{} ({})".format(self.checklist_name, self.get_checklist_type_display())

    class Meta:
        unique_together = [("checklist_name",)]

    def load(self, page=None):
        from flora.util import seinet_util, inat_util, local_flora_util

        if self.checklist_type == checklist_types.ChecklistTypeChoices.SEINET:
            seinet_util.SEINETChecklistReader(self).load_checklist(page=page)
        elif self.checklist_type == checklist_types.ChecklistTypeChoices.INAT:
            inat_util.InatChecklistReader(self).load_checklist()
        elif self.checklist_type == checklist_types.ChecklistTypeChoices.FLORA:
            local_flora_util.LocalFloraReader(self).load_checklist()

    def read_specific_record_data(self, records):
        from flora.util import seinet_util, inat_util

        if self.checklist_type == checklist_types.ChecklistTypeChoices.SEINET:
            seinet_util.SEINETRecordReader(self).read_records(records=records)
        elif self.checklist_type == checklist_types.ChecklistTypeChoices.INAT:
            inat_util.InatRecordsReader(self).read_records(records=records)

    def read_record_data(self, limit=10):
        from flora.util import seinet_util, inat_util

        if self.checklist_type == checklist_types.ChecklistTypeChoices.SEINET:
            seinet_util.SEINETRecordReader(self).read_records(limit=limit)
        elif self.checklist_type == checklist_types.ChecklistTypeChoices.INAT:
            inat_util.InatRecordsReader(self).read_records(limit=limit)

    def missing_dates(self):
        if self.latest_date_retrieved is not None:
            start_date = self.latest_date_retrieved
        elif self.earliest_year is not None:
            start_date = timezone.datetime(
                year=int(self.earliest_year), month=1, day=1
            ).date()
        else:
            return

        end_date = timezone.now().date() - timezone.timedelta(days=2)
        yield from date_util.combine_date_ranges(
            list(date_util.date_range_list(start_date, end_date))
        )

    def stale_records(self):
        from flora import models

        checklist_type = self.checklist_type

        if checklist_type == "i":
            records = models.InatRecord
        elif checklist_type == "s":
            records = models.SEINETRecord
        elif checklist_type == "f":
            records = models.FloraRecord
        else:
            raise ValueError

        return records.objects.filter(
            Q(last_refreshed__isnull=True) | Q(last_refreshed__lt=timezone.now() - timezone.timedelta(days=60)),
            checklist_taxon__checklist=self,
            is_placeholder=False,
        )
