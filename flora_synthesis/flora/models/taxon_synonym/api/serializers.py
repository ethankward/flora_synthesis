from rest_framework import serializers

from flora import models


class TaxonSynonymSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TaxonSynonym
        fields = ['id', 'taxon', 'synonym']
