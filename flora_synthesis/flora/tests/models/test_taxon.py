from django.test import TestCase

from flora import models
from flora.models.taxon.choices import taxon_ranks
from flora.tests import factory


class TaxonTests(TestCase):
    def test_synonymize_parent_sub(self):
        t1 = factory.TaxonFactory(taxon_name="Acmispon oroboides",
                                  rank=taxon_ranks.TaxonRankChoices.SPECIES)
        t2 = factory.TaxonFactory(taxon_name="Acmispon oroboides var. oroboides",
                                  rank=taxon_ranks.TaxonRankChoices.VARIETY,
                                  parent_species=t1)
        t1.subtaxa.add(t2)

        t3 = factory.TaxonFactory(taxon_name="Lotus oroboides",
                                  rank=taxon_ranks.TaxonRankChoices.SPECIES)
        t1.synonymize(t3)

        self.assertEqual(2, models.Taxon.objects.all().count())
        t2 = models.Taxon.objects.get(pk=t2.pk)
        self.assertEqual(t2.parent_species, t3)
        self.assertEqual(1, t3.subtaxa.all().count())
        self.assertTrue(t2 in t3.subtaxa.all())
