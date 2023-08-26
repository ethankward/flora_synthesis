from django.test import TestCase

from flora.tests import factory


class ChecklistTaxonTests(TestCase):
    def test_save(self):
        taxon_1 = factory.TaxonFactory()
        taxon_2 = factory.TaxonFactory()

        checklist_taxon = factory.ChecklistTaxonFactory(checklist_taxon_name="x")
        checklist_taxon.taxa.add(taxon_1)
        checklist_taxon.taxa.add(taxon_2)

        self.assertTrue(taxon_1 in checklist_taxon.taxa.all())
        self.assertTrue(taxon_2 in checklist_taxon.taxa.all())
        checklist_taxon.save()
        taxa = list(checklist_taxon.taxa.all())
        self.assertFalse(taxon_1 in taxa)
        self.assertFalse(taxon_2 in taxa)
        self.assertEqual(1, len(taxa))
        self.assertEqual("X", taxa[0].taxon_name)

        checklist_taxon_2 = factory.ChecklistTaxonFactory(checklist_taxon_name="Bouteloua trifida var. trifida")
        taxa = list(checklist_taxon_2.taxa.all())
        self.assertEqual(2, len(taxa))
