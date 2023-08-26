import factory

from flora import models


class TaxonFamilyFactory(factory.django.DjangoModelFactory):
    family = factory.Sequence(lambda n: "family {}".format(n))

    class Meta:
        model = models.TaxonFamily


class TaxonGenusFactory(factory.django.DjangoModelFactory):
    genus = factory.Sequence(lambda n: "genus {}".format(n))

    class Meta:
        model = models.TaxonGenus


class TaxonFactory(factory.django.DjangoModelFactory):
    genus = factory.SubFactory(TaxonGenusFactory)
    family = factory.SubFactory(TaxonFamilyFactory)
    taxon_name = factory.Sequence(lambda n: "taxon {}".format(n))

    class Meta:
        model = models.Taxon


class TaxonSynonymFactory(factory.django.DjangoModelFactory):
    taxon = factory.SubFactory(TaxonFactory)
    synonym = factory.Sequence(lambda n: "synonym {}".format(n))

    class Meta:
        model = models.TaxonSynonym


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
    checklist_taxon_name = factory.Sequence(lambda n: "checklist taxon {}".format(n))
    checklist_taxon_family = factory.SubFactory(ChecklistTaxonFamilyFactory)

    class Meta:
        model = models.ChecklistTaxon


class ChecklistRecordFactory(factory.django.DjangoModelFactory):
    checklist = factory.SubFactory(ChecklistFactory)
    checklist_taxon = factory.SubFactory(ChecklistTaxonFactory)

    class Meta:
        model = models.ChecklistRecord
