from rest_framework import serializers

from flora import models


class ChecklistSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Checklist
        fields = ['id', 'checklist_name', 'checklist_type', 'checklist_state', 'external_checklist_id', 'locality',
                  'latest_date_retrieved', 'earliest_year']


class TaxonNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Taxon
        fields = ['id', 'taxon_name']


class ChecklistTaxonSerializer(serializers.ModelSerializer):
    family = serializers.SerializerMethodField()
    all_mapped_taxa = TaxonNameSerializer(many=True)

    class Meta:
        model = models.ChecklistTaxon
        fields = ['id', 'taxon_name', 'family', 'external_id', 'rank', 'genus', 'checklist', 'all_mapped_taxa']

    def get_family(self, obj):
        return obj.family.family


class LifeCycleSerializer(serializers.Serializer):
    value = serializers.CharField()
    display = serializers.CharField()


class EndemicSerializer(serializers.Serializer):
    value = serializers.CharField()
    display = serializers.CharField()


class IntroducedSerializer(serializers.Serializer):
    value = serializers.CharField()
    display = serializers.CharField()


class TaxonSynonymSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TaxonSynonym
        fields = ['id', 'taxon', 'synonym']

    def update(self, instance, validated_data):
        instance.synonym = validated_data.get('synonym', instance.synonym)
        instance.save()
        return instance


class ChecklistTaxonFamilySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ChecklistTaxonFamily
        fields = ['id', 'family', 'checklist', 'external_id']


class ChecklistTaxonNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ChecklistTaxon
        fields = ['id', 'taxon_name']



class ObservationDateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ObservationDate
        fields = ['date', 'url']


class MinimalTaxonSerializer(serializers.ModelSerializer):
    life_cycle = serializers.SerializerMethodField(read_only=False)
    endemic = serializers.SerializerMethodField(read_only=False)
    introduced = serializers.SerializerMethodField(read_only=False)
    first_observation_date = ObservationDateSerializer()
    last_observation_date = ObservationDateSerializer()

    class Meta:
        model = models.Taxon
        fields = ['id', 'taxon_name', 'rank', 'genus', 'family',
                  'life_cycle', 'endemic', 'introduced',
                  'seinet_id', 'inat_id', 'first_observation_date', 'last_observation_date']

    def get_life_cycle(self, obj):
        return {'value': obj.life_cycle, 'display': obj.get_life_cycle_display()}

    def get_endemic(self, obj):
        return {'value': obj.endemic, 'display': obj.get_endemic_display()}

    def get_introduced(self, obj):
        return {'value': obj.introduced, 'display': obj.get_introduced_display()}


class TaxonSerializer(serializers.ModelSerializer):
    synonyms = serializers.SerializerMethodField(read_only=False)
    taxon_checklist_taxa = ChecklistTaxonSerializer(many=True)
    parent_species = TaxonNameSerializer()
    subtaxa = TaxonNameSerializer(many=True)

    life_cycle_display = serializers.CharField(source='get_life_cycle_display')
    endemic_display = serializers.CharField(source='get_endemic_display')
    introduced_display = serializers.CharField(source='get_introduced_display')

    rank = serializers.SerializerMethodField()
    checklists = serializers.SerializerMethodField()
    first_observation_date = ObservationDateSerializer()
    last_observation_date = ObservationDateSerializer()

    class Meta:
        model = models.Taxon
        fields = ['id', 'taxon_name', 'rank', 'genus', 'family', 'parent_species', 'subtaxa',
                  'synonyms',
                  'life_cycle', 'life_cycle_display',
                  'endemic', 'endemic_display',
                  'introduced', 'introduced_display',
                  'seinet_id', 'inat_id',
                  'taxon_checklist_taxa', 'checklists',
                  'first_observation_date', 'last_observation_date']

    def get_synonyms(self, obj):
        synonyms = obj.taxonsynonym_set.all()
        return [{'value': s.id, 'display': s.synonym} for s in synonyms]

    def get_rank(self, obj):
        return obj.get_rank_display()

    def get_checklists(self, obj):
        return sorted(set([checklist_taxon.checklist.pk for checklist_taxon in obj.taxon_checklist_taxa.all()]))

    def get_observation_dates(self, obj):
        return []

    def update(self, instance, validated_data):
        instance.family = validated_data.get('family', instance.family)
        instance.life_cycle = validated_data.get('life_cycle', instance.life_cycle)
        instance.endemic = validated_data.get('endemic', instance.endemic)
        instance.introduced = validated_data.get('introduced', instance.introduced)
        instance.taxon_name = validated_data.get('taxon_name', instance.taxon_name)
        instance.seinet_id = validated_data.get('seinet_id', instance.seinet_id)
        instance.inat_id = validated_data.get('inat_id', instance.inat_id)

        instance.save()
        return instance


class ChecklistRecordSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    external_id = serializers.CharField()
    last_refreshed = serializers.DateTimeField()
    checklist_taxon = ChecklistTaxonNameSerializer()
    mapped_taxon = TaxonNameSerializer()
    checklist = ChecklistSerializer()
    date = serializers.DateField()
    observer = serializers.CharField()
    external_url = serializers.URLField()
    observation_type = serializers.CharField()
