from rest_framework import serializers

from flora import models


class ChecklistSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Checklist
        fields = [
            "id",
            "checklist_name",
            "checklist_type",
            "checklist_state",
            "external_checklist_id",
            "locality",
            "latest_date_retrieved",
            "earliest_year",
            "primary_checklist",
            "citation",
            "citation_url",
        ]


class ChecklistStaleRecordCount(serializers.ModelSerializer):
    stale_record_count = serializers.SerializerMethodField()

    class Meta:
        model = models.Checklist
        fields = ["id", "stale_record_count"]

    def get_stale_record_count(self, obj):
        return obj.stale_records().count()


class ChecklistStaleRecordsSerializer(serializers.ModelSerializer):
    from flora.models.records.api.serializers import ChecklistRecordSerializer

    stale_records = ChecklistRecordSerializer(many=True)

    class Meta:
        model = models.Checklist
        fields = ['id', 'stale_records']

    def get_stale_records(self, obj):
        return obj.stale_records()
