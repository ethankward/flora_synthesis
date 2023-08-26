from django.urls import include, path
from rest_framework import routers

from flora import api

router = routers.DefaultRouter()

router.register(r"taxa", api.views.TaxonViewSet)
router.register(r"taxon_synonyms", api.views.TaxonSynonymViewSet)
router.register(r"checklists", api.views.ChecklistViewSet)
router.register(r"checklist_records", api.views.ChecklistRecordViewSet)
router.register(r"checklist_record_images", api.views.ChecklistRecordImagesViewSet)
router.register(r"observation_types", api.views.ObservationTypeViewSet)
router.register(r"checklist_families", api.views.ChecklistFamilyViewSet)
router.register(r"checklist_taxa", api.views.ChecklistTaxonViewSet)

urlpatterns = [
    path("api/", include(router.urls)),
    path('api/life_cycles/', api.views.LifeCycleView.as_view(), name="life_cycles"),
    path('api/endemic/', api.views.EndemicView.as_view(), name="endemic")
]
