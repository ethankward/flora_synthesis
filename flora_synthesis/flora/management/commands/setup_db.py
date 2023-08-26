from django.core.management import BaseCommand
from django.db import transaction

from flora import models
from flora.util import taxon_util


def load_data(fn):
    result = open("flora/data/{}.txt".format(fn)).read().split('\n')
    return [i.split('\t') for i in result]


def add_observation_types():
    for observation_type, observation_type_value in models.ObservationTypeChoices.choices:
        ot, _ = models.ObservationType.objects.get_or_create(observation_type=observation_type)
        ot.observation_type_value = observation_type_value
        ot.save()


def import_synonyms():
    data = load_data("synonyms")

    for taxon_name, synonym, family in data:
        taxon = taxon_util.TaxonName(taxon_name, family=family).get_db_item()
        s_db, _ = models.TaxonSynonym.objects.get_or_create(synonym=synonym, taxon=taxon)
        s_db.taxon = taxon
        s_db.save()


def import_endemic():
    data = load_data("endemic")

    for taxon_name, endemic_status, family in data:
        taxon = taxon_util.TaxonName(taxon_name, family=family).get_db_item()
        taxon.endemic = endemic_status
        taxon.save()


def import_introduced():
    data = load_data("introduced")

    for taxon_name, introduced_status, family in data:
        taxon = taxon_util.TaxonName(taxon_name, family=family).get_db_item()
        taxon.introduced = introduced_status
        taxon.save()


def import_life_cycles():
    data = load_data("life_cycles")

    for taxon_name, life_cycle, family in data:
        taxon = taxon_util.TaxonName(taxon_name, family=family).get_db_item()
        taxon.life_cycle = life_cycle
        taxon.save()


class Command(BaseCommand):
    def handle(self, *args, **options):
        with transaction.atomic():
            add_observation_types()
            import_synonyms()
            import_endemic()
            import_introduced()
            import_life_cycles()
