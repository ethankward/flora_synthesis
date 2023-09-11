from django.urls import path
from rest_framework import routers

from flora.models.checklist.api import views


def get_urlpatterns(router: routers.DefaultRouter):
    router.register(r"checklists", views.ChecklistViewSet)
    router.register(r"checklist_stale_record_counts", views.ChecklistStaleRecordCountViewSet)

    return [
        path('api/update_checklist/', views.update, name="update_checklist"),
        path('api/retrieve_checklist/', views.retrieve, name="retrieve_checklist"),
    ]
