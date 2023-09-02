from django.test import TestCase

from flora import models
from flora.models.taxon.choices import taxon_ranks
from flora.tests import factory
from flora.util import taxon_name_util


class TaxonNameTests(TestCase):
    def test_single_word(self):
        self.assertRaises(ValueError, lambda: taxon_name_util.TaxonName("Heterotheca"))

    def test_species(self):
        t1 = taxon_name_util.TaxonName("Heterotheca marginata")
        self.assertEqual(t1.rank, taxon_ranks.TaxonRankChoices.SPECIES)
        self.assertEqual(t1.canonical_name, 'Heterotheca marginata')
        self.assertEqual(t1.genus, 'Heterotheca')

        t2 = taxon_name_util.TaxonName(" a    b  ")
        self.assertEqual(t2.rank, taxon_ranks.TaxonRankChoices.SPECIES)
        self.assertEqual(t2.canonical_name, 'A b')
        self.assertEqual(t2.genus, 'A')

    def test_3_part(self):
        self.assertRaises(ValueError, lambda: taxon_name_util.TaxonName("a b c"))

        t1 = taxon_name_util.TaxonName("a b c", given_rank=taxon_ranks.TaxonRankChoices.VARIETY)
        self.assertEqual(t1.rank, taxon_ranks.TaxonRankChoices.VARIETY)
        self.assertEqual(t1.canonical_name, 'A b var. c')
        self.assertEqual(t1.genus, 'A')
        self.assertEqual(t1.parent_species_name, 'A b')

        t2 = taxon_name_util.TaxonName("x y z", given_rank=taxon_ranks.TaxonRankChoices.SUBSPECIES)
        self.assertEqual(t2.rank, taxon_ranks.TaxonRankChoices.SUBSPECIES)
        self.assertEqual(t2.canonical_name, 'X y subsp. z')
        self.assertEqual(t2.genus, 'X')
        self.assertEqual(t2.parent_species_name, 'X y')

    def test_4_part(self):
        self.assertRaises(ValueError, lambda: taxon_name_util.TaxonName("a b c d"))
        self.assertRaises(ValueError, lambda: taxon_name_util.TaxonName("a b var. d",
                                                                        given_rank=taxon_ranks.TaxonRankChoices.SUBSPECIES))
        self.assertRaises(ValueError, lambda: taxon_name_util.TaxonName("a b subsp. d",
                                                                        given_rank=taxon_ranks.TaxonRankChoices.VARIETY))
        self.assertRaises(ValueError, lambda: taxon_name_util.TaxonName("a b × d",
                                                                        given_rank=taxon_ranks.TaxonRankChoices.VARIETY))

        t1 = taxon_name_util.TaxonName("a b var. c")
        self.assertEqual(t1.rank, taxon_ranks.TaxonRankChoices.VARIETY)
        self.assertEqual(t1.canonical_name, 'A b var. c')
        self.assertEqual(t1.genus, 'A')
        self.assertEqual(t1.parent_species_name, 'A b')

        t2 = taxon_name_util.TaxonName("a b subsp. c")
        self.assertEqual(t2.rank, taxon_ranks.TaxonRankChoices.SUBSPECIES)
        self.assertEqual(t2.canonical_name, 'A b subsp. c')
        self.assertEqual(t2.genus, 'A')
        self.assertEqual(t2.parent_species_name, 'A b')

        t3 = taxon_name_util.TaxonName("a b × c")
        self.assertEqual(t3.rank, taxon_ranks.TaxonRankChoices.HYBRID)
        self.assertEqual(t3.canonical_name, 'A b × c')
        self.assertEqual(t3.genus, 'A')
        self.assertEqual(t3.parent_species_name, None)

        t4 = taxon_name_util.TaxonName("a b x c")
        self.assertEqual(t4.rank, taxon_ranks.TaxonRankChoices.HYBRID)
        self.assertEqual(t4.canonical_name, 'A b × c')
        self.assertEqual(t4.genus, 'A')
        self.assertEqual(t4.parent_species_name, None)

    def test_5_part(self):
        self.assertRaises(ValueError, lambda: taxon_name_util.TaxonName("a b c d e"))

        t1 = taxon_name_util.TaxonName("a b x c d")
        self.assertEqual(t1.rank, taxon_ranks.TaxonRankChoices.HYBRID)
        self.assertEqual(t1.canonical_name, 'A b × c d')
        self.assertEqual(t1.genus, 'A')
        self.assertEqual(t1.parent_species_name, None)

    def test_6_part(self):
        self.assertRaises(ValueError, lambda: taxon_name_util.TaxonName("a b x c x d"))

        t1 = taxon_name_util.TaxonName("a b subsp. c var. d")
        self.assertEqual(t1.rank, taxon_ranks.TaxonRankChoices.SUBSPECIES_VARIETY)
        self.assertEqual(t1.canonical_name, 'A b subsp. c var. d')
        self.assertEqual(t1.genus, 'A')
        self.assertEqual(t1.parent_species_name, 'A b')

    def test_get_db_item_synonym(self):
        taxon = factory.TaxonFactory(taxon_name='Platanus wrightii')
        factory.TaxonSynonymFactory(synonym='Phacelia crenulata', taxon=taxon)

        t1 = taxon_name_util.TaxonName("Phacelia crenulata").get_db_item()
        self.assertEqual(t1.taxon_name, "Platanus wrightii")

    def test_get_db_item_existing(self):
        factory.TaxonFactory(taxon_name='Platanus wrightii')
        self.assertEqual(1, models.Taxon.objects.all().count())
        t1 = taxon_name_util.TaxonName("Platanus wrightii").get_db_item()
        self.assertEqual(1, models.Taxon.objects.all().count())
        self.assertEqual(t1.taxon_name, "Platanus wrightii")

    def test_get_db_item_new(self):
        self.assertEqual(0, models.Taxon.objects.all().count())
        t1 = taxon_name_util.TaxonName("A b var. c", family="Asteraceae").get_db_item()
        self.assertEqual(2, models.Taxon.objects.all().count())
        self.assertEqual(t1.taxon_name, "A b var. c")
        self.assertEqual(t1.parent_species.taxon_name, "A b")
        self.assertEqual(t1.parent_species.family, "Asteraceae")
