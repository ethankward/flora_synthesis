from django.urls import path
from rest_framework import routers

from flora.models.taxon.api import views


def get_urlpatterns(router: routers.DefaultRouter):
    router.register(r"taxa_autocomplete", views.TaxonAutocompleteViewSet)
    router.register(r"primary_taxa", views.PrimaryChecklistTaxonViewSet, basename="primary_taxa")
    router.register(r"taxa", views.TaxonViewSet, basename="taxa")

    return [
        path('api/taxon_families/', views.FamiliesListView.as_view(), name="taxon_families"),
        path('api/life_cycles/', views.LifeCycleView.as_view(), name="life_cycles"),
        path('api/endemic/', views.EndemicView.as_view(), name="endemic"),
        path('api/introduced/', views.IntroducedView.as_view(), name="introduced"),
        path('api/taxon_ranks/', views.RankChoicesView.as_view(), name="ranks"),
        path('api/make_synonym_of/', views.make_synonym_of),
        path('api/update_computed_values/', views.update_computed_values, name="update_computed_values"),
        path('api/create_new_taxon/', views.create_new_taxon),
    ]
