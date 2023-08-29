from django.db import models

from flora.models import base_model


class TaxonRankChoices(models.TextChoices):
    SPECIES = 'S', 'Species'
    SUBSPECIES = 'U', 'Subspecies'
    VARIETY = 'V', 'Variety'
    SUBSPECIES_VARIETY = 'Q', 'Subspecies variety'
    HYBRID = 'H', 'Hybrid'


class LifeCycleChoices(models.TextChoices):
    a = 'a', 'Annual'
    p = 'p', 'Perennial'
    u = 'u', 'Unknown'


class IntroducedChoices(models.TextChoices):
    introduced = 'i', 'introduced'
    native = 'n', 'native'
    possibly_introduced = 'p', 'possibly introduced'


class EndemicChoices(models.TextChoices):
    n = "n", "Not endemic"
    u = "u", "In the US only in Rincons but also occurs outside of the US"
    z = "z", "In Arizona only found in Rincons but also occurs outside of Arizona"
    a = "a", "Only found in Arizona"
    r = "r", "Only found in Rincons"


class Taxon(base_model.BaseModel):
    taxon_name = models.CharField(max_length=256)

    rank = models.CharField(max_length=1, choices=TaxonRankChoices.choices)
    genus = models.CharField(max_length=256)
    family = models.CharField(max_length=256)

    parent_species = models.ForeignKey("Taxon", blank=True, null=True, on_delete=models.SET_NULL,
                                       related_name="taxon_parent_species")
    subtaxa = models.ManyToManyField("Taxon", blank=True, related_name="taxon_subtaxa")

    life_cycle = models.CharField(max_length=1, blank=True, null=True, choices=LifeCycleChoices.choices)
    introduced = models.CharField(max_length=1, choices=IntroducedChoices.choices, blank=True, null=True)
    endemic = models.CharField(max_length=1, choices=EndemicChoices.choices, blank=True, null=True)

    inat_id = models.IntegerField(blank=True, null=True)
    seinet_id = models.IntegerField(blank=True, null=True)

    class Meta:
        unique_together = [('taxon_name',)]

    def __str__(self):
        return self.taxon_name
