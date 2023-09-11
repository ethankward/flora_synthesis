from rest_framework import routers

from flora.models.checklist_taxon_family.api import views


def get_urlpatterns(router: routers.DefaultRouter):
    router.register(r"checklist_taxon_families", views.ChecklistTaxonFamilyViewSet)

    return []
