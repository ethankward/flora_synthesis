from django.urls import path
from rest_framework import routers

from flora.models.checklist.api import views


def get_urlpatterns(router: routers.DefaultRouter):
    router.register(r"checklists", views.ChecklistViewSet, basename="checklists")
    router.register(
        r"checklist_stale_record_counts",
        views.ChecklistStaleRecordCountViewSet,
        basename="checklist_stale_record_counts",
    )

    return [
        path("api/load_checklist/", views.load_checklist, name="load_checklist"),
        path("api/retrieve_checklist/", views.retrieve_records, name="retrieve_records"),
        path(
            "api/import_inat_observation/",
            views.import_inat_observation,
            name="import_inat_observation",
        ),
    ]
