import json

from django.test import TestCase

from flora import models
from flora.tests import factory
from flora.util import local_flora_util


class ChecklistUtilUpdateTests(TestCase):
    def test_local_flora_update(self):
        t1 = factory.TaxonFactory(taxon_name="A b")
        t2 = factory.TaxonFactory(taxon_name="B c")

        checklist_record = factory.FloraRecordFactory(mapped_taxon=t1,
                                                      full_metadata=json.dumps(
                                                          {"mapped_taxon_name": "B c", "observation_type": "True"}))

        updater = local_flora_util.LocalFloraUpdater(record=checklist_record)
        updater.update_record()

        checklist_record = models.FloraRecord.objects.get(pk=checklist_record.pk)
        self.assertEqual(checklist_record.mapped_taxon, t1)

    def test_local_flora_update_mapped_taxon_null(self):
        checklist_record = factory.FloraRecordFactory(mapped_taxon=None,
                                                      full_metadata=json.dumps(
                                                          {"mapped_taxon_name": None, "observation_type": "True"}))

        updater = local_flora_util.LocalFloraUpdater(record=checklist_record)
        updater.update_record()

        checklist_record = models.FloraRecord.objects.get(pk=checklist_record.pk)
        self.assertIsNone(checklist_record.mapped_taxon)
