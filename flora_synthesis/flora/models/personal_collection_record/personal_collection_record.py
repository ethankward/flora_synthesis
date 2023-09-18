from django.db import models


class StatusTypes(models.TextChoices):
    p = "p", "Personal collection"
    h = "h", "Submitted to herbarium"


class PersonalCollectionRecord(models.Model):
    collection_number = models.IntegerField()
    date = models.DateField()
    family = models.CharField(max_length=256)
    status = models.CharField(max_length=1, choices=StatusTypes.choices)
    preliminary_taxon = models.CharField(max_length=256)

    inat_record_id = models.IntegerField(blank=True, null=True)
    seinet_record_id = models.IntegerField(blank=True, null=True)

    specific_taxon = models.ForeignKey("Taxon", blank=True, null=True, on_delete=models.SET_NULL)

    latitude = models.DecimalField(max_digits=32, decimal_places=12, blank=True, null=True)
    longitude = models.DecimalField(max_digits=32, decimal_places=12, blank=True, null=True)

    elevation_ft = models.IntegerField(blank=True, null=True)
    time = models.TimeField(blank=True, null=True)

    locality = models.TextField(blank=True, null=True)
    habitat = models.TextField(blank=True, null=True)
    associated_collectors = models.TextField(blank=True, null=True)

    associated_species = models.TextField(blank=True, null=True)

    identification_notes = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    land_ownership = models.TextField(blank=True, null=True)
