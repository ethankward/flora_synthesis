import factory

from flora import models


class ChecklistFactory(factory.django.DjangoModelFactory):
    checklist_name = factory.Sequence(lambda n: "checklist {}".format(n))

    class Meta:
        model = models.Checklist


class ChecklistTaxonFamilyFactory(factory.django.DjangoModelFactory):
    family = factory.Sequence(lambda n: "family {}".format(n))
    checklist = factory.SubFactory(ChecklistFactory)

    class Meta:
        model = models.ChecklistTaxonFamily


class ChecklistTaxonFactory(factory.django.DjangoModelFactory):
    checklist = factory.SubFactory(ChecklistFactory)
    taxon_name = factory.Sequence(lambda n: "checklist taxon {}".format(n))
    family = factory.SubFactory(ChecklistTaxonFamilyFactory)

    class Meta:
        model = models.ChecklistTaxon


class TaxonFactory(factory.django.DjangoModelFactory):
    taxon_name = factory.Sequence(lambda n: "taxon {}".format(n))

    class Meta:
        model = models.Taxon


class TaxonSynonymFactory(factory.django.DjangoModelFactory):
    taxon = factory.SubFactory(TaxonFactory)
    synonym = factory.Sequence(lambda n: "synonym {}".format(n))

    class Meta:
        model = models.TaxonSynonym


class FloraRecordFactory(factory.django.DjangoModelFactory):
    checklist = factory.SubFactory(ChecklistFactory)
    external_id = factory.Sequence(lambda n: "flora_record_{}".format(n))
    checklist_taxon = factory.SubFactory(ChecklistTaxonFactory)
    mapped_taxon = factory.SubFactory(TaxonFactory)

    class Meta:
        model = models.FloraRecord


class SEINETRecordFactory(factory.django.DjangoModelFactory):
    checklist = factory.SubFactory(ChecklistFactory)

    external_id = factory.Sequence(lambda n: "seinet_record_{}".format(n))
    checklist_taxon = factory.SubFactory(ChecklistTaxonFactory)
    mapped_taxon = factory.SubFactory(TaxonFactory)

    class Meta:
        model = models.SEINETRecord


class InatRecordFactory(factory.django.DjangoModelFactory):
    checklist = factory.SubFactory(ChecklistFactory)

    external_id = factory.Sequence(lambda n: "seinet_record_{}".format(n))
    checklist_taxon = factory.SubFactory(ChecklistTaxonFactory)
    mapped_taxon = factory.SubFactory(TaxonFactory)

    class Meta:
        model = models.InatRecord
