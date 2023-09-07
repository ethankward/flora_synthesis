from django.test import TestCase

from flora import models
from flora.tests import factory

from flora.util import checklist_util
from flora.util import local_flora_util

class TaxonTests(TestCase):
    def test_update_mapped_taxon(self):
        t1 = factory.TaxonFactory(taxon_name="A b")
        t2 = factory.TaxonFactory(taxon_name="B c")

        record = factory.FloraRecordFactory(mapped_taxon=t1)

        self.assertEqual(record.mapped_taxon, t1)
        record.mapped_taxon = t2
        self.assertEqual(record.mapped_taxon, t2)
        record.save()
        record.checklist_taxon.save()

        record = models.FloraRecord.objects.get(pk=record.pk, )
        self.assertEqual(record.mapped_taxon, t2)

        updater = local_flora_util.LocalFloraUpdater(record=record)
