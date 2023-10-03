from rest_framework import serializers

from flora import models


class ChecklistTaxonFamilySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ChecklistTaxonFamily
        fields = ["id", "family", "checklist", "external_id"]
