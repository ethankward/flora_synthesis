from rest_framework import viewsets

from flora import models
from flora.models.collector_alias.api import serializers


class CollectorAliasViewset(viewsets.ModelViewSet):
    queryset = models.CollectorAlias.objects.all()
    serializer_class = serializers.CollectorAliasSerializer
