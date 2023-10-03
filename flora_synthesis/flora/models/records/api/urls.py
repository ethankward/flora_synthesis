from django.urls import path
from rest_framework import routers

from flora.models.records.api import views


def get_urlpatterns(router: routers.DefaultRouter):
    return [
        path(
            "api/update_checklist_record_mapping/",
            views.update_checklist_record_mapped_taxon,
        ),
        path(
            "api/checklist_records/<str:checklist_type>/<int:checklist_record_id>/",
            views.ChecklistRecordView.as_view(),
            name="checklist_record",
        ),
        path(
            "api/checklist_records/",
            views.ChecklistRecordsView.as_view(),
            name="checklist_records",
        ),
        path(
            "api/checklist_records_no_collector",
            views.ChecklistRecordNoCollectionsView.as_view(),
            name="checklist_records_no_collector",
        ),
    ]
