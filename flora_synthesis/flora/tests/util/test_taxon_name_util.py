from django.test import TestCase

from flora import models
from flora.models.taxon.choices import taxon_ranks
from flora.tests import factory
from flora.util import taxon_name_util


class TaxonNameTests(TestCase):
    def test_single_word(self):
        """Test a single genus name without any given rank."""
        self.assertRaises(ValueError, lambda: taxon_name_util.TaxonName("Heterotheca"))

    def test_species(self):
        """Test species name is recognized without any given rank."""
        t1 = taxon_name_util.TaxonName("Heterotheca marginata")
        self.assertEqual(t1.rank, taxon_ranks.TaxonRankChoices.SPECIES)
        self.assertEqual(t1.canonical_name, "Heterotheca marginata")
        self.assertEqual(t1.genus, "Heterotheca")

        t2 = taxon_name_util.TaxonName(" a    b  ")
        self.assertEqual(t2.rank, taxon_ranks.TaxonRankChoices.SPECIES)
        self.assertEqual(t2.canonical_name, "A b")
        self.assertEqual(t2.genus, "A")

    def test_3_part(self):
        """Test 3 part names (varieties, subspecies)."""
        self.assertRaises(ValueError, lambda: taxon_name_util.TaxonName("a b c"))

        t1 = taxon_name_util.TaxonName(
            "a b c", given_rank=taxon_ranks.TaxonRankChoices.VARIETY
        )
        self.assertEqual(t1.rank, taxon_ranks.TaxonRankChoices.VARIETY)
        self.assertEqual(t1.canonical_name, "A b var. c")
        self.assertEqual(t1.genus, "A")
        self.assertEqual(t1.parent_species_name, "A b")

        t2 = taxon_name_util.TaxonName(
            "x y z", given_rank=taxon_ranks.TaxonRankChoices.SUBSPECIES
        )
        self.assertEqual(t2.rank, taxon_ranks.TaxonRankChoices.SUBSPECIES)
        self.assertEqual(t2.canonical_name, "X y subsp. z")
        self.assertEqual(t2.genus, "X")
        self.assertEqual(t2.parent_species_name, "X y")

    def test_4_part(self):
        """Test 4 part names (variety, subspecies)."""
        self.assertRaises(ValueError, lambda: taxon_name_util.TaxonName("a b c d"))
        self.assertRaises(
            ValueError,
            lambda: taxon_name_util.TaxonName(
                "a b var. d", given_rank=taxon_ranks.TaxonRankChoices.SUBSPECIES
            ),
        )
        self.assertRaises(
            ValueError,
            lambda: taxon_name_util.TaxonName(
                "a b subsp. d", given_rank=taxon_ranks.TaxonRankChoices.VARIETY
            ),
        )
        self.assertRaises(
            ValueError,
            lambda: taxon_name_util.TaxonName(
                "a b × d", given_rank=taxon_ranks.TaxonRankChoices.VARIETY
            ),
        )

        t1 = taxon_name_util.TaxonName("a b var. c")
        self.assertEqual(t1.rank, taxon_ranks.TaxonRankChoices.VARIETY)
        self.assertEqual(t1.canonical_name, "A b var. c")
        self.assertEqual(t1.genus, "A")
        self.assertEqual(t1.parent_species_name, "A b")

        t2 = taxon_name_util.TaxonName("a b subsp. c")
        self.assertEqual(t2.rank, taxon_ranks.TaxonRankChoices.SUBSPECIES)
        self.assertEqual(t2.canonical_name, "A b subsp. c")
        self.assertEqual(t2.genus, "A")
        self.assertEqual(t2.parent_species_name, "A b")

        t3 = taxon_name_util.TaxonName("a b × c")
        self.assertEqual(t3.rank, taxon_ranks.TaxonRankChoices.HYBRID)
        self.assertEqual(t3.canonical_name, "A b × c")
        self.assertEqual(t3.genus, "A")
        self.assertEqual(t3.parent_species_name, None)

        t4 = taxon_name_util.TaxonName("a b x c")
        self.assertEqual(t4.rank, taxon_ranks.TaxonRankChoices.HYBRID)
        self.assertEqual(t4.canonical_name, "A b × c")
        self.assertEqual(t4.genus, "A")
        self.assertEqual(t4.parent_species_name, None)

    def test_5_part(self):
        """Test 5 part hybrid names."""
        self.assertRaises(ValueError, lambda: taxon_name_util.TaxonName("a b c d e"))

        t1 = taxon_name_util.TaxonName("a b x c d")
        self.assertEqual(t1.rank, taxon_ranks.TaxonRankChoices.HYBRID)
        self.assertEqual(t1.canonical_name, "A b × c d")
        self.assertEqual(t1.genus, "A")
        self.assertEqual(t1.parent_species_name, None)

    def test_6_part(self):
        """Test 6 part names (variety of a subspecies)."""
        self.assertRaises(ValueError, lambda: taxon_name_util.TaxonName("a b x c x d"))

        t1 = taxon_name_util.TaxonName("a b subsp. c var. d")
        self.assertEqual(t1.rank, taxon_ranks.TaxonRankChoices.SUBSPECIES_VARIETY)
        self.assertEqual(t1.canonical_name, "A b subsp. c var. d")
        self.assertEqual(t1.genus, "A")
        self.assertEqual(t1.parent_species_name, "A b")

    def test_get_db_item_synonym(self):
        """Test getting a taxon name that has a synonym."""
        taxon = factory.TaxonFactory(taxon_name="Platanus wrightii")
        factory.TaxonSynonymFactory(synonym="Phacelia crenulata", taxon=taxon)

        t1 = taxon_name_util.TaxonName("Phacelia crenulata").get_db_item()
        self.assertEqual(t1.taxon_name, "Platanus wrightii")

    def test_get_db_item_existing(self):
        """Test getting an already existing name."""
        factory.TaxonFactory(taxon_name="Platanus wrightii")
        self.assertEqual(1, models.Taxon.objects.all().count())
        t1 = taxon_name_util.TaxonName("Platanus wrightii").get_db_item()
        self.assertEqual(1, models.Taxon.objects.all().count())
        self.assertEqual(t1.taxon_name, "Platanus wrightii")

    def test_get_db_item_new(self):
        """Test creating name with parent taxon."""
        self.assertEqual(0, models.Taxon.objects.all().count())
        t1 = taxon_name_util.TaxonName("A b var. c", family="Asteraceae").get_db_item()
        self.assertEqual(2, models.Taxon.objects.all().count())
        self.assertEqual(t1.taxon_name, "A b var. c")
        self.assertEqual(t1.parent_species.taxon_name, "A b")
        self.assertEqual(t1.parent_species.family, "Asteraceae")

    def test_name_sp(self):
        """Test genus name format."""
        t1 = taxon_name_util.TaxonName("Heterotheca sp.", family="Asteraceae")
        self.assertEqual(t1.rank, taxon_ranks.TaxonRankChoices.GENUS)
        self.assertEqual(t1.canonical_name, "Heterotheca sp.")

    def test_hybrid_with_rank(self):
        """Test hybrid name with rank."""
        t1 = taxon_name_util.TaxonName(
            "Apocynum x floribundum",
            family="Apocynaceae",
            given_rank=taxon_ranks.TaxonRankChoices.HYBRID,
        )
        self.assertEqual(t1.canonical_name, "Apocynum × floribundum")

    def test_hybrid_4(self):
        """Test hybrid 4 part format."""
        t1 = taxon_name_util.TaxonName(
            "a b x c",
            family="Apocynaceae",
            given_rank=taxon_ranks.TaxonRankChoices.HYBRID,
        )
        self.assertEqual(t1.canonical_name, "A b × c")

    def test_hybrid_5(self):
        """Test hybrid 5 part format."""
        t1 = taxon_name_util.TaxonName("a b × c d")
        self.assertEqual(t1.canonical_name, "A b × c d")
