from rest_framework import viewsets

from flora import models
from flora.models.checklist_taxon.api import serializers


class ChecklistTaxonViewSet(viewsets.ModelViewSet):
    queryset = models.ChecklistTaxon.objects.all().select_related('family')
    serializer_class = serializers.ChecklistTaxonSerializer
