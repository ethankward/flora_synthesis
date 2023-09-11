from rest_framework import serializers

from flora import models


class ChecklistSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Checklist
        fields = ['id', 'checklist_name', 'checklist_type', 'checklist_state', 'external_checklist_id', 'locality',
                  'latest_date_retrieved', 'earliest_year']
