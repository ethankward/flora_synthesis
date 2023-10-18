from rest_framework import serializers

from flora import models
from flora.models.checklist_taxon.api.serializers import ChecklistTaxonSerializer


class TaxonNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Taxon
        fields = ["id", "taxon_name"]


class TaxonSerializer(serializers.ModelSerializer):
    synonyms = serializers.SerializerMethodField(read_only=False)
    taxon_checklist_taxa = ChecklistTaxonSerializer(many=True, read_only=True)
    parent_species = TaxonNameSerializer(read_only=True)
    subtaxa = TaxonNameSerializer(many=True, read_only=True)

    life_cycle_display = serializers.CharField(source="get_life_cycle_display")
    endemic_display = serializers.CharField(source="get_endemic_display")
    introduced_display = serializers.CharField(source="get_introduced_display")

    rank = serializers.SerializerMethodField()
    checklists = serializers.SerializerMethodField()
    primary_checklist = serializers.SerializerMethodField()

    class Meta:
        model = models.Taxon
        fields = [
            "id",
            "taxon_name",
            "rank",
            "genus",
            "family",
            "parent_species",
            "subtaxa",
            "synonyms",
            "life_cycle",
            "life_cycle_display",
            "endemic",
            "endemic_display",
            "introduced",
            "introduced_display",
            "seinet_id",
            "inat_id",
            "taxon_checklist_taxa",
            "checklists",
            "first_observation_date",
            "last_observation_date",
            "first_observation_date_url",
            "last_observation_date_url",
            "local_population_strict_northern_range_limit",
            "local_population_strict_eastern_range_limit",
            "local_population_strict_western_range_limit",
            "local_population_strict_southern_range_limit",
            "local_population_northern_edge_range_limit",
            "local_population_eastern_edge_range_limit",
            "local_population_western_edge_range_limit",
            "local_population_southern_edge_range_limit",
            "local_population_disjunct",
            "has_collections",
            "primary_checklist",
            "occurrence_remarks",
            "author"
        ]

    def get_synonyms(self, obj):
        synonyms = obj.taxonsynonym_set.all()
        return [{"value": s.id, "display": s.synonym} for s in synonyms]

    def get_primary_checklist(self, obj):
        for checklist_taxon in obj.taxon_checklist_taxa.all():
            if checklist_taxon.checklist.primary_checklist:
                return True
        return False

    def get_rank(self, obj):
        return obj.get_rank_display()

    def get_checklists(self, obj):
        return sorted(
            set(
                [
                    checklist_taxon.checklist.pk
                    for checklist_taxon in obj.taxon_checklist_taxa.all()
                ]
            )
        )

    def get_observation_dates(self, obj):
        return []


class MinimalTaxonSerializer(serializers.ModelSerializer):
    life_cycle = serializers.SerializerMethodField(read_only=False)
    endemic = serializers.SerializerMethodField(read_only=False)
    introduced = serializers.SerializerMethodField(read_only=False)

    class Meta:
        model = models.Taxon
        fields = [
            "id",
            "taxon_name",
            "rank",
            "genus",
            "family",
            "life_cycle",
            "endemic",
            "introduced",
            "seinet_id",
            "inat_id",
            "first_observation_date",
            "last_observation_date",
            "first_observation_date_url",
            "last_observation_date_url",
            "local_population_strict_northern_range_limit",
            "local_population_strict_eastern_range_limit",
            "local_population_strict_western_range_limit",
            "local_population_strict_southern_range_limit",
            "local_population_northern_edge_range_limit",
            "local_population_eastern_edge_range_limit",
            "local_population_western_edge_range_limit",
            "local_population_southern_edge_range_limit",
            "local_population_disjunct",
            "author"
        ]

    def get_life_cycle(self, obj):
        return {"value": obj.life_cycle, "display": obj.get_life_cycle_display()}

    def get_endemic(self, obj):
        return {"value": obj.endemic, "display": obj.get_endemic_display()}

    def get_introduced(self, obj):
        return {"value": obj.introduced, "display": obj.get_introduced_display()}


class TaxonFamilySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    family = serializers.CharField()


class LifeCycleSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    value = serializers.CharField()
    display = serializers.CharField()


class EndemicSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    value = serializers.CharField()
    display = serializers.CharField()


class IntroducedSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    value = serializers.CharField()
    display = serializers.CharField()
