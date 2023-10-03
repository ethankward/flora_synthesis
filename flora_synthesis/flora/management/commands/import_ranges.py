from django.core.management import BaseCommand
from django.db import transaction

from flora import models


def get_bool_prop(s):
    if s == "y":
        return True
    elif s == "n":
        return False


def run():
    data = open("flora/data/ranges.txt").read().split("\n")
    data = [i.split("\t") for i in data]

    all_taxon_names = {taxon.taxon_name: taxon for taxon in models.Taxon.objects.all()}

    with transaction.atomic():
        for q in data:
            if len(q) == 5:
                taxon_name, north, south, east, west = q
                if " (" in taxon_name:
                    taxon_name = taxon_name.split(" (")[0]

                if taxon_name in all_taxon_names:
                    taxon = all_taxon_names[taxon_name]
                    taxon.local_population_strict_northern_range_limit = get_bool_prop(
                        north
                    )
                    taxon.local_population_strict_southern_range_limit = get_bool_prop(
                        south
                    )
                    taxon.local_population_strict_eastern_range_limit = get_bool_prop(
                        east
                    )
                    taxon.local_population_strict_western_range_limit = get_bool_prop(
                        west
                    )
                    taxon.save()
                else:
                    print(taxon_name)


class Command(BaseCommand):
    def handle(self, *args, **options):
        run()
