from rest_framework import viewsets

from flora import models
from flora.models.checklist_taxon_family.api import serializers


class ChecklistTaxonFamilyViewSet(viewsets.ModelViewSet):
    queryset = models.ChecklistTaxonFamily.objects.all()
    serializer_class = serializers.ChecklistTaxonFamilySerializer
