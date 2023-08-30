from django.db import models

from flora.models import base_model
from flora.models.taxon.choices import taxon_introduced_statuses, taxon_life_cycles, taxon_endemic_statuses, taxon_ranks


class Taxon(base_model.BaseModel):
    taxon_name = models.CharField(max_length=256)

    rank = models.CharField(max_length=1, choices=taxon_ranks.TaxonRankChoices.choices)
    genus = models.CharField(max_length=256)
    family = models.CharField(max_length=256)

    parent_species = models.ForeignKey("Taxon", blank=True, null=True, on_delete=models.SET_NULL,
                                       related_name="taxon_parent_species")
    subtaxa = models.ManyToManyField("Taxon", blank=True, related_name="taxon_subtaxa")

    life_cycle = models.CharField(max_length=1,
                                  blank=True,
                                  null=True,
                                  choices=taxon_life_cycles.LifeCycleChoices.choices)
    introduced = models.CharField(max_length=1,
                                  choices=taxon_introduced_statuses.IntroducedChoices.choices,
                                  blank=True,
                                  null=True)
    endemic = models.CharField(max_length=1,
                               choices=taxon_endemic_statuses.EndemicChoices.choices,
                               blank=True,
                               null=True)

    inat_id = models.IntegerField(blank=True, null=True)
    seinet_id = models.IntegerField(blank=True, null=True)

    class Meta:
        unique_together = [('taxon_name',)]

    def __str__(self):
        return self.taxon_name
