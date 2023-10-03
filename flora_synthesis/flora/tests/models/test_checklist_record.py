from django.test import TestCase

from flora import models
from flora.models.records.inat_record.choices import (
    observation_types as inat_observation_types,
)
from flora.tests import factory
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

        record = models.FloraRecord.objects.get(pk=record.pk)
        self.assertEqual(record.mapped_taxon, t2)

        updater = local_flora_util.LocalFloraUpdater(record=record)

    def test_exclude_inat_casual(self):
        taxon = factory.TaxonFactory()

        i1 = factory.InatRecordFactory(
            observation_type=inat_observation_types.InatObservationTypeChoices.RESEARCH,
            mapped_taxon=taxon,
            active=True,
        )
        self.assertTrue(i1.active)
        self.assertTrue(taxon in i1.checklist_taxon.all_mapped_taxa.all())

        i2 = factory.InatRecordFactory(
            observation_type=inat_observation_types.InatObservationTypeChoices.CASUAL,
            mapped_taxon=taxon,
            active=True,
        )
        self.assertFalse(i2.active)
        self.assertFalse(taxon in i2.checklist_taxon.all_mapped_taxa.all())
