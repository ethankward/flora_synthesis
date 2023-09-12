from django.db.models import Q
from django.utils import timezone
from rest_framework import serializers

from flora import models


class ChecklistSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Checklist
        fields = ['id', 'checklist_name', 'checklist_type', 'checklist_state', 'external_checklist_id', 'locality',
                  'latest_date_retrieved', 'earliest_year', 'primary_checklist']


class ChecklistStaleRecordCount(serializers.ModelSerializer):
    stale_record_count = serializers.SerializerMethodField()

    class Meta:
        model = models.Checklist
        fields = ['id', 'stale_record_count']

    def get_stale_record_count(self, obj):
        if obj.checklist_type == 'i':
            records = models.InatRecord
        elif obj.checklist_type == 's':
            records = models.SEINETRecord
        elif obj.checklist_type == 'f':
            records = models.FloraRecord
        else:
            raise ValueError

        return records.objects.filter(
            Q(last_refreshed__isnull=True) | Q(last_refreshed__lt=timezone.now() - timezone.timedelta(days=60)),
            checklist_taxon__checklist=obj, is_placeholder=False).count()
