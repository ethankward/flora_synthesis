from rest_framework import viewsets

from flora import models
from flora.models.collector.api import serializers


class CollectorViewset(viewsets.ModelViewSet):
    queryset = models.Collector.objects.all().prefetch_related('collector_aliases',
                                                               'collector_seinet_collection_records',
                                                               'collector_seinet_collection_records__checklist_taxon').order_by(
        'name')
    serializer_class = serializers.CollectorSerializer
