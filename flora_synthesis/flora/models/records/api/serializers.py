from rest_framework import serializers

from flora.models.checklist.api.serializers import ChecklistSerializer
from flora.models.checklist_record_note.api.serializers import ChecklistRecordNoteSerializer
from flora.models.checklist_taxon.api.serializers import ChecklistTaxonNameSerializer
from flora.models.taxon.api.serializers import TaxonNameSerializer


class ChecklistRecordSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    external_id = serializers.CharField()
    last_refreshed = serializers.DateTimeField()
    checklist_taxon = ChecklistTaxonNameSerializer()
    mapped_taxon = TaxonNameSerializer()
    checklist = ChecklistSerializer()
    date = serializers.DateField()
    observer = serializers.CharField()
    external_url = serializers.URLField()
    observation_type = serializers.CharField()
    notes = ChecklistRecordNoteSerializer(many=True)
    active = serializers.BooleanField()
