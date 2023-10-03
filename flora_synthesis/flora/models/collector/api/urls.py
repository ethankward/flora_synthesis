from rest_framework import routers

from flora.models.collector.api import views


def get_urlpatterns(router: routers.DefaultRouter):
    router.register(r"collectors", views.CollectorViewset, basename="collectors")
    router.register(
        r"collector_list", views.CollectorListViewset, basename="collector_list"
    )

    return []
