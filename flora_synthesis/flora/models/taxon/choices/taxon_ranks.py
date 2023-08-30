from django.db import models


class TaxonRankChoices(models.TextChoices):
    SPECIES = 'S', 'Species'
    SUBSPECIES = 'U', 'Subspecies'
    VARIETY = 'V', 'Variety'
    SUBSPECIES_VARIETY = 'Q', 'Subspecies variety'
    HYBRID = 'H', 'Hybrid'
