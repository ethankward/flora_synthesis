from rest_framework.exceptions import APIException
from rest_framework.request import Request

from flora import models
from flora.util import api_crud


def update_checklist_record_note(
    note_to_update: models.ChecklistRecordNote, request: Request
):
    note_text = request.data["note"]
    note_to_update.note = note_text


def create_checklist_record_note(request):
    checklist_record_id = request.data["checklist_record_id"]
    checklist_type = request.data["checklist_record_type"]
    note = request.data["note"]

    if checklist_type == "f":
        record = models.FloraRecord.objects.get(pk=checklist_record_id)
    elif checklist_type == "s":
        record = models.SEINETRecord.objects.get(pk=checklist_record_id)
    elif checklist_type == "i":
        record = models.InatRecord.objects.get(pk=checklist_record_id)
    else:
        raise APIException()

    note = models.ChecklistRecordNote(note=note)
    note.save()
    record.notes.add(note)

    return note


crud_generator = api_crud.CRUDViewGenerator(
    model=models.ChecklistRecordNote,
    model_name="checklist_record_note",
    creation_function=create_checklist_record_note,
    update_function=update_checklist_record_note,
)
