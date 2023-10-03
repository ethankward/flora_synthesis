from rest_framework import viewsets
from rest_framework.exceptions import APIException
from rest_framework.mixins import UpdateModelMixin

from flora import models
from flora.models.checklist_record_note.api import serializers


class ChecklistRecordNoteViewSet(viewsets.ModelViewSet, UpdateModelMixin):
    queryset = models.ChecklistRecordNote.objects.all()
    serializer_class = serializers.ChecklistRecordNoteSerializer

    def create(self, request, *args, **kwargs):
        result = super().create(request, *args, **kwargs)

        checklist_type = request.data.get("checklist_record_type", None)
        checklist_record_id = request.data.get("checklist_record_id", None)

        note = models.ChecklistRecordNote.objects.get(pk=result.data['id'])

        if checklist_type is not None and checklist_record_id is not None:
            if checklist_type == "f":
                record = models.FloraRecord.objects.get(pk=checklist_record_id)
            elif checklist_type == "s":
                record = models.SEINETRecord.objects.get(pk=checklist_record_id)
            elif checklist_type == "i":
                record = models.InatRecord.objects.get(pk=checklist_record_id)
            else:
                raise APIException()
            record.notes.add(note)

        return result
