from rest_framework import routers

from flora.models.collector_alias.api import views


def get_urlpatterns(router: routers.DefaultRouter):
    router.register(
        r"collector_aliases", views.CollectorAliasViewset, basename="collector_aliases"
    )

    return []
