from rest_framework import routers

from flora.models.herbarium_report.api import views


def get_urlpatterns(router: routers.DefaultRouter):
    router.register(
        r"herbarium_reports", views.HerbariumReportViewset, basename="herbarium_reports"
    )

    return []
