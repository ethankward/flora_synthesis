from django.db import models

from flora.models import base_model
from flora.models.taxon.choices import (
    taxon_introduced_statuses,
    taxon_life_cycles,
    taxon_endemic_statuses,
    taxon_ranks,
)
from flora.util import merge_objects


class Taxon(base_model.BaseModel):
    taxon_name: str = models.CharField(max_length=256)

    rank: str = models.CharField(max_length=1, choices=taxon_ranks.TaxonRankChoices.choices)
    genus: str = models.CharField(max_length=256)
    family: str = models.CharField(max_length=256)

    parent_species = models.ForeignKey(
        "Taxon",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="taxon_parent_species",
    )
    subtaxa = models.ManyToManyField("Taxon", blank=True, related_name="taxon_subtaxa")

    life_cycle = models.CharField(
        max_length=1,
        blank=True,
        null=True,
        choices=taxon_life_cycles.LifeCycleChoices.choices,
    )
    introduced = models.CharField(
        max_length=1,
        choices=taxon_introduced_statuses.IntroducedChoices.choices,
        blank=True,
        null=True,
    )
    endemic = models.CharField(
        max_length=1,
        choices=taxon_endemic_statuses.EndemicChoices.choices,
        blank=True,
        null=True,
    )

    inat_id = models.IntegerField(blank=True, null=True)
    seinet_id = models.IntegerField(blank=True, null=True)

    # computed values
    first_observation_date = models.DateField(blank=True, null=True)
    first_observation_date_url = models.URLField(blank=True, null=True)
    last_observation_date = models.DateField(blank=True, null=True)
    last_observation_date_url = models.URLField(blank=True, null=True)

    has_collections = models.BooleanField(blank=True, null=True)

    # population distribution
    local_population_strict_northern_range_limit = models.BooleanField(
        blank=True, null=True
    )
    local_population_strict_eastern_range_limit = models.BooleanField(
        blank=True, null=True
    )
    local_population_strict_western_range_limit = models.BooleanField(
        blank=True, null=True
    )
    local_population_strict_southern_range_limit = models.BooleanField(
        blank=True, null=True
    )

    local_population_northern_edge_range_limit = models.BooleanField(
        blank=True, null=True
    )
    local_population_eastern_edge_range_limit = models.BooleanField(
        blank=True, null=True
    )
    local_population_western_edge_range_limit = models.BooleanField(
        blank=True, null=True
    )
    local_population_southern_edge_range_limit = models.BooleanField(
        blank=True, null=True
    )

    local_population_disjunct = models.BooleanField(blank=True, null=True)

    occurrence_remarks = models.TextField(blank=True, null=True)

    author = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = [("taxon_name",)]
        indexes = [
            models.Index(fields=["taxon_name"]),
            models.Index(fields=["family", "taxon_name"]),
        ]

    def __str__(self):
        return self.taxon_name

    def save(self, *args, **kwargs):
        self.genus = self.taxon_name.split(" ")[0]
        super().save(*args, **kwargs)

    def synonymize(self, taxon):
        from flora.models import TaxonSynonym

        to_delete_taxon_id = self.pk
        to_merge_into_taxon_id = taxon.pk

        taxon_to_delete = Taxon.objects.get(pk=to_delete_taxon_id)
        taxon_to_merge_into = Taxon.objects.get(pk=to_merge_into_taxon_id)

        assert to_delete_taxon_id != to_merge_into_taxon_id

        old_taxon_name = taxon_to_delete.taxon_name

        synonym, _ = TaxonSynonym.objects.get_or_create(
            taxon=taxon_to_merge_into, synonym=old_taxon_name
        )

        merge_objects.merge_objects(taxon_to_delete, taxon_to_merge_into)
