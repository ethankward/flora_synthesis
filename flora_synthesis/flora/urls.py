from django.urls import include, path
from rest_framework import routers

from flora import api

router = routers.DefaultRouter()
router.register(r"taxa", api.views.TaxonViewSet, basename="taxa")
router.register(r"taxon_synonyms", api.views.TaxonSynonymViewSet)
router.register(r"taxa_autocomplete", api.views.TaxonAutocompleteViewSet)
router.register(r"checklists", api.views.ChecklistViewSet)
router.register(r"checklist_taxon_families", api.views.ChecklistTaxonFamilyViewSet)
router.register(r"checklist_taxa", api.views.ChecklistTaxonViewSet)

urlpatterns = [
    path("api/", include(router.urls)),
    path('api/life_cycles/', api.views.LifeCycleView.as_view(), name="life_cycles"),
    path('api/endemic/', api.views.EndemicView.as_view(), name="endemic"),
    path('api/make_synonym_of/', api.views.make_synonym_of),
    path('api/checklist_records/<str:checklist_type>/<int:checklist_record_id>/', api.views.ChecklistRecordView.as_view(),
         name='checklist_record'),
    path('api/checklist_records/', api.views.ChecklistRecordsView.as_view(),
         name='checklist_records')
]
