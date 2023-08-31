from django.core.management import BaseCommand
from django.db import transaction

from flora import models
from flora.models.taxon.util import handle_taxon_name


def load_data(fn):
    result = open("flora/data/{}.txt".format(fn)).read().split('\n')
    return [i.split('\t') for i in result]


def import_synonyms():
    data = load_data("synonyms")

    for taxon_name, synonym, family in data:
        taxon = handle_taxon_name.TaxonName(taxon_name, family=family).get_db_item()
        s_db, _ = models.TaxonSynonym.objects.get_or_create(synonym=synonym, taxon=taxon)
        s_db.taxon = taxon
        s_db.save()


def import_endemic():
    data = load_data("endemic")

    for taxon_name, endemic_status, family in data:
        taxon = handle_taxon_name.TaxonName(taxon_name, family=family).get_db_item()
        taxon.endemic = endemic_status
        taxon.save()


def import_introduced():
    data = load_data("introduced")

    for taxon_name, introduced_status, family in data:
        taxon = handle_taxon_name.TaxonName(taxon_name, family=family).get_db_item()
        taxon.introduced = introduced_status
        taxon.save()


def import_life_cycles():
    data = load_data("life_cycles")

    for taxon_name, life_cycle, family in data:
        taxon = handle_taxon_name.TaxonName(taxon_name, family=family).get_db_item()
        taxon.life_cycle = life_cycle
        taxon.save()


class Command(BaseCommand):
    def handle(self, *args, **options):
        with transaction.atomic():
            import_synonyms()
            import_endemic()
            import_introduced()
            import_life_cycles()
