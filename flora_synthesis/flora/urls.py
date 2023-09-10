from django.urls import include, path
from rest_framework import routers

from flora import api

router = routers.DefaultRouter()
router.register(r"taxa", api.views.TaxonViewSet, basename="taxa")
router.register(r"primary_taxa", api.views.PrimaryChecklistTaxonViewSet, basename="primary_taxa")
router.register(r"taxon_synonyms", api.views.TaxonSynonymViewSet)
router.register(r"taxa_autocomplete", api.views.TaxonAutocompleteViewSet)
router.register(r"checklists", api.views.ChecklistViewSet)
router.register(r"checklist_taxon_families", api.views.ChecklistTaxonFamilyViewSet)
router.register(r"checklist_taxa", api.views.ChecklistTaxonViewSet)

urlpatterns = [
    path("api/", include(router.urls)),
    path('api/life_cycles/', api.views.LifeCycleView.as_view(), name="life_cycles"),
    path('api/endemic/', api.views.EndemicView.as_view(), name="endemic"),
    path('api/introduced/', api.views.IntroducedView.as_view(), name="introduced"),
    path('api/make_synonym_of/', api.views.make_synonym_of),
    path('api/create_new_synonym/', api.views.create_new_synonym),
    path('api/delete_taxon_synonym/', api.views.delete_taxon_synonym),

    path('api/update_checklist_record_mapping/', api.views.update_checklist_record_mapped_taxon),
    path('api/checklist_records/<str:checklist_type>/<int:checklist_record_id>/',
         api.views.ChecklistRecordView.as_view(),
         name='checklist_record'),
    path('api/checklist_records/', api.views.ChecklistRecordsView.as_view(),
         name='checklist_records'),

    path('api/create_new_checklist_record_note/', api.views.create_new_checklist_record_note),
    path('api/delete_checklist_record_note/', api.views.delete_checklist_record_note),
    path('api/update_checklist_record_note/', api.views.update_checklist_record_note),

]
