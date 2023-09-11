from rest_framework import serializers

from flora import models


class TaxonNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Taxon
        fields = ['id', 'taxon_name']


class ChecklistTaxonNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ChecklistTaxon
        fields = ['id', 'taxon_name']


class ChecklistTaxonSerializer(serializers.ModelSerializer):
    family = serializers.SerializerMethodField()
    all_mapped_taxa = TaxonNameSerializer(many=True)

    class Meta:
        model = models.ChecklistTaxon
        fields = ['id', 'taxon_name', 'family', 'external_id', 'rank', 'genus', 'checklist', 'all_mapped_taxa']

    def get_family(self, obj):
        return obj.family.family
