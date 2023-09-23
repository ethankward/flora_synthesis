from rest_framework import viewsets

from flora import models
from flora.models.taxon_synonym.api import serializers


class TaxonSynonymViewSet(viewsets.ModelViewSet):
    queryset = models.TaxonSynonym.objects.all()
    serializer_class = serializers.TaxonSynonymSerializer
