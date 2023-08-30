from django.db import models, transaction

from flora.models import base_model


class TaxonSynonym(base_model.BaseModel):
    taxon = models.ForeignKey("Taxon", on_delete=models.CASCADE)
    synonym = models.CharField(max_length=256)

    class Meta:
        unique_together = [('synonym',)]

    def save(self, *args, **kwargs):
        from flora.util import taxon_util
        from flora.models import Taxon
        super().save(*args, **kwargs)

        with transaction.atomic():
            to_merge = list(Taxon.objects.filter(taxon_name=self.synonym))

            for taxon in to_merge:
                if taxon != self.taxon:
                    taxon_util.make_synonym_of(taxon, self.taxon)
