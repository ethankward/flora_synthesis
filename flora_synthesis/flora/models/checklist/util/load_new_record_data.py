from django.db.models import Q
from django.utils import timezone

from flora import models
from flora.models.checklist.choices import checklist_types
from flora.models.records.inat_record.util import read_inat_records
from flora.models.records.seinet_record.util import read_seinet_records


def load_new_seinet_data(checklist):
    old_records = models.SEINETRecord.objects.filter(
        Q(last_refreshed__isnull=True) | Q(last_refreshed__lt=timezone.now() - timezone.timedelta(days=60)),
        checklist_taxon__checklist=checklist,
        is_placeholder=False
    ).order_by('?')

    print('loading new records', old_records.count())
    read_seinet_records.SEINETRecordReader(records=old_records[:10]).read_records()


def load_new_inat_data(checklist):
    old_records = models.InatRecord.objects.filter(
        Q(last_refreshed__isnull=True) | Q(last_refreshed__lt=timezone.now() - timezone.timedelta(days=60)),
        checklist_taxon__checklist=checklist,
    ).order_by('?')

    print('loading new records', old_records.count())

    read_inat_records.InatRecordsReader(records=old_records[:10]).read_records()


def load_new_record_data(checklist):
    if checklist.checklist_type == checklist_types.ChecklistTypeChoices.SEINET:
        load_new_seinet_data(checklist)
    elif checklist.checklist_type == checklist_types.ChecklistTypeChoices.INAT:
        load_new_inat_data(checklist)
