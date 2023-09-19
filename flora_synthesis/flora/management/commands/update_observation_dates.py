from django.core.management import BaseCommand
from django.db import transaction

from flora import models


def run():
    print('Updating observation dates')
    mapped_records = {}
    record_models = [models.InatRecord, models.SEINETRecord]
    for record_model in record_models:
        for record in record_model.objects.filter(mapped_taxon__isnull=False, checklist__primary_checklist=True,
                                                  date__isnull=False).select_related('mapped_taxon',
                                                                                     'mapped_taxon__parent_species'):
            taxon = record.mapped_taxon
            if taxon not in mapped_records:
                mapped_records[taxon] = set([])
            mapped_records[taxon].add((record.date, record.external_url()))

            parent_taxon = taxon.parent_species
            if parent_taxon is not None:
                if parent_taxon not in mapped_records:
                    mapped_records[parent_taxon] = set([])
                mapped_records[parent_taxon].add((record.date, record.external_url()))

    print('{} taxa with dates'.format(len(mapped_records)))

    with transaction.atomic():
        models.Taxon.objects.all().update(first_observation_date=None, last_observation_date=None,
                                          first_observation_date_url=None, last_observation_date_url=None)
        for taxon in mapped_records:
            dates = sorted(mapped_records[taxon])
            if dates:
                taxon.first_observation_date = dates[0][0]
                taxon.first_observation_date_url = dates[0][1]
                taxon.last_observation_date = dates[-1][0]
                taxon.last_observation_date_url = dates[-1][1]
                taxon.save()

    print('Finished update')


class Command(BaseCommand):
    def handle(self, *args, **options):
        run()
