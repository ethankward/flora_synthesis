from rest_framework import routers

from flora.models.checklist_record_note.api import views


def get_urlpatterns(router: routers.DefaultRouter):
    router.register(r"checklist_record_notes", views.ChecklistRecordNoteViewSet, basename="checklist_record_notes")
    return []
