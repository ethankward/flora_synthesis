from django.db.models import F
from rest_framework import viewsets
from rest_framework.mixins import UpdateModelMixin

from flora import models
from flora.models.collector.api import serializers


class CollectorListViewset(viewsets.ModelViewSet):
    queryset = models.Collector.objects.all().order_by(
        F("first_collection_year").asc(nulls_last=True), "name"
    )
    serializer_class = serializers.CollectorListSerializer


class CollectorViewset(viewsets.ModelViewSet, UpdateModelMixin):
    queryset = (
        models.Collector.objects.all()
        .prefetch_related(
            "collector_aliases",
            "collector_seinet_collection_records",
            "collector_seinet_collection_records__checklist_taxon",
        )
        .order_by("name")
    )
    serializer_class = serializers.CollectorSerializer

    def get_serializer(self, *args, **kwargs):
        if self.request.method == "GET":
            return serializers.CollectorSerializer(*args, **kwargs)
        else:
            return serializers.CollectorUpdateSerializer(*args, **kwargs)
