from django.urls import path, include
from rest_framework import routers

from flora.models.checklist.api import urls as checklist_urls
from flora.models.checklist_record_note.api import urls as checklist_record_note_urls
from flora.models.checklist_taxon.api import urls as checklist_taxon_urls
from flora.models.checklist_taxon_family.api import urls as checklist_taxon_family_urls
from flora.models.collector.api import urls as collector_urls
from flora.models.collector_alias.api import urls as collector_alias_urls
from flora.models.personal_collection_record.api import urls as personal_collection_record_urls
from flora.models.records.api import urls as records_urls
from flora.models.taxon.api import urls as taxon_urls
from flora.models.taxon_synonym.api import urls as taxon_synonym_urls

all_url_modules = [checklist_urls, checklist_record_note_urls, checklist_taxon_urls, checklist_taxon_family_urls,
                   records_urls, taxon_urls, taxon_synonym_urls, personal_collection_record_urls, collector_urls,
                   collector_alias_urls]

router = routers.DefaultRouter()

urlpatterns = []

for module in all_url_modules:
    urlpatterns.extend(module.get_urlpatterns(router))

urlpatterns.append(path("api/", include(router.urls)))
