from django.urls import path
from rest_framework import routers

from flora.models.checklist.api import views


def get_urlpatterns(router: routers.DefaultRouter):
    router.register(r"checklists", views.ChecklistViewSet, basename="checklists")
    router.register(r"checklist_stale_record_counts", views.ChecklistStaleRecordCountViewSet,
                    basename="checklist_stale_record_counts")

    return [
        path('api/update_checklist/', views.update, name="update_checklist"),
        path('api/retrieve_checklist/', views.retrieve, name="retrieve_checklist"),
        path('api/import_inat_observation/', views.import_inat_observation, name="import_inat_observation")
    ]
