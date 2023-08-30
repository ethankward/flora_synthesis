from rest_framework import serializers

from flora import models


class ChecklistSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Checklist
        fields = ['id', 'checklist_name', 'checklist_type', 'checklist_state', 'external_checklist_id', 'locality',
                  'latest_date_retrieved', 'earliest_year']


class ChecklistTaxonSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ChecklistTaxon
        fields = ['id', 'taxon_name', 'family', 'external_id', 'rank', 'genus', 'checklist']

#
# class LifeCycleSerializer(serializers.Serializer):
#     value = serializers.CharField()
#     text = serializers.CharField()
#
#
# class EndemicSerializer(serializers.Serializer):
#     value = serializers.CharField()
#     text = serializers.CharField()
#
#
# class TaxonSynonymSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.TaxonSynonym
#         fields = ['pk', 'taxon', 'synonym']
#
#
#
#
# class ChecklistFamilySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.ChecklistTaxonFamily
#         fields = ['pk', 'family', 'checklist', 'external_id']
#
#
# class ChecklistTaxonNameSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.ChecklistTaxon
#         fields = ['pk', 'taxon_name']
#
#

# class TaxonNameSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.Taxon
#         fields = ['pk', 'taxon_name']
#
#
# class TaxonSerializer(serializers.ModelSerializer):
#     taxonsynonym_set = TaxonSynonymSerializer(many=True)
#     taxon_checklist_taxa = ChecklistTaxonSerializer(many=True)
#     parent_species = TaxonNameSerializer()
#     subtaxa = TaxonNameSerializer(many=True)
#     life_cycle_values = serializers.SerializerMethodField(read_only=False)
#     endemic_values = serializers.SerializerMethodField(read_only=False)
#
#     rank = serializers.SerializerMethodField()
#
#     class Meta:
#         model = models.Taxon
#         fields = ['pk', 'taxon_name', 'rank', 'genus', 'family', 'life_cycle', 'parent_species', 'subtaxa',
#                   'taxonsynonym_set', 'endemic', 'endemic_values', 'introduced',
#                   'life_cycle_values', 'life_cycle',
#                   'seinet_id', 'inat_id', 'taxon_checklist_taxa', 'endemic_values']
#
#     def get_life_cycle_values(self, obj):
#         return (obj.life_cycle, obj.get_life_cycle_display())
#
#     def get_endemic_values(self, obj):
#         return (obj.endemic, obj.get_endemic_display())
#
#     def get_rank(self, obj):
#         return obj.get_rank_display()
#
#     def update(self, instance, validated_data):
#         instance.family = validated_data.get('family', instance.family)
#         instance.life_cycle = validated_data.get('life_cycle', instance.life_cycle)
#         instance.endemic = validated_data.get('endemic', instance.endemic)
#         instance.taxon_name = validated_data.get('taxon_name', instance.taxon_name)
#         instance.seinet_id = validated_data.get('seinet_id', instance.seinet_id)
#         instance.inat_id = validated_data.get('inat_id', instance.inat_id)
#
#         instance.save()
#         return instance

#
# class ChecklistRecordSerializer(serializers.ModelSerializer):
#     checklist = ChecklistSerializer()
#     checklist_taxon = ChecklistTaxonNameSerializer()
#     canonical_mapped_taxon = TaxonNameSerializer()
#     external_url = serializers.SerializerMethodField()
#
#     class Meta:
#         model = models.ChecklistRecord
#         fields = ['pk', 'checklist', 'checklist_taxon', 'canonical_mapped_taxon', 'external_record_id',
#                   'observation_type',
#                   'last_refreshed', 'external_url', 'date', 'observer', 'active', 'placeholder']
#
#     def get_external_url(self, obj):
#         return obj.external_url()
