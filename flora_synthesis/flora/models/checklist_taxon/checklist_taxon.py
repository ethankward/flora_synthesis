import itertools

from django.db import models

from flora.models import base_model


class ChecklistTaxon(base_model.BaseModel):
    checklist = models.ForeignKey("Checklist", on_delete=models.CASCADE)

    taxon_name = models.CharField(max_length=256)
    family = models.ForeignKey("ChecklistTaxonFamily", on_delete=models.CASCADE)
    genus = models.CharField(max_length=256, blank=True, null=True)

    external_id = models.IntegerField(blank=True, null=True)
    rank = models.CharField(max_length=256, blank=True, null=True)

    all_mapped_taxa = models.ManyToManyField("Taxon", blank=True, related_name="taxon_checklist_taxa")

    class Meta:
        unique_together = [('checklist', 'taxon_name')]

    def save(self, *args, **kwargs):
        from flora import models

        if self.pk is not None:
            self.all_mapped_taxa.clear()

            seinet_records = models.SEINETRecord.objects.filter(checklist_taxon=self, active=True)
            inat_records = models.InatRecord.objects.filter(checklist_taxon=self, active=True)
            flora_records = models.FloraRecord.objects.filter(checklist_taxon=self, active=True)

            for record in itertools.chain(seinet_records, inat_records, flora_records):
                mapped_taxon = record.mapped_taxon
                if mapped_taxon is not None:
                    parent = mapped_taxon.parent_species
                    self.all_mapped_taxa.add(mapped_taxon)
                    if parent is not None:
                        self.all_mapped_taxa.add(parent)

        super().save(*args, **kwargs)
