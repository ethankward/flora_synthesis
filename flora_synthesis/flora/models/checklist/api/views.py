from rest_framework import viewsets

from flora import models
from flora.models.checklist.api import serializers


class ChecklistViewSet(viewsets.ModelViewSet):
    queryset = models.Checklist.objects.all()
    serializer_class = serializers.ChecklistSerializer
