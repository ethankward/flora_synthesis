from rest_framework import routers

from flora.models.checklist_taxon.api import views


def get_urlpatterns(router: routers.DefaultRouter):
    router.register(r"checklist_taxa", views.ChecklistTaxonViewSet)

    return []
