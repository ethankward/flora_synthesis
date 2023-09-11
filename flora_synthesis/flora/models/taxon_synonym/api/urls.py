from rest_framework import routers

from flora.models.taxon_synonym.api import views


def get_urlpatterns(router: routers.DefaultRouter):
    router.register(r"taxon_synonyms", views.TaxonSynonymViewSet)

    return views.crud_generator.get_urlpatterns()
