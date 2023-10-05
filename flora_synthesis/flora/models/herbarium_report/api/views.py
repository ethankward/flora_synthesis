from rest_framework import viewsets

from flora import models
from flora.models.herbarium_report.api import serializers


class HerbariumReportViewset(viewsets.ModelViewSet):
    queryset = models.HerbariumReport.objects.all()
    serializer_class = serializers.HerbariumReportSerializer
