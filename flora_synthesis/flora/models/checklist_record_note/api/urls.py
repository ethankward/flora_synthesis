from rest_framework import routers

from flora.models.checklist_record_note.api import views


def get_urlpatterns(router: routers.DefaultRouter):
    return views.crud_generator.get_urlpatterns()
