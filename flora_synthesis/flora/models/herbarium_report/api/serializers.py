from rest_framework import serializers

from flora import models


class HerbariumReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.HerbariumReport
        fields = ["id", "taxon", "url"]
