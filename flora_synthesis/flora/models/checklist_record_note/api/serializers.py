from rest_framework import serializers

from flora import models


class ChecklistRecordNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ChecklistRecordNote
        fields = ['id', 'note', 'added_on']
