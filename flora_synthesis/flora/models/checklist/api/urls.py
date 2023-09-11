from rest_framework import routers

from flora.models.checklist.api import views


def get_urlpatterns(router: routers.DefaultRouter):
    router.register(r"checklists", views.ChecklistViewSet)

    return []
