from django.core.management import BaseCommand
from django.db import transaction

from flora import models


def run():
    mapped_records = {}
    record_models = [models.InatRecord, models.SEINETRecord]
    for record_model in record_models:
        for record in record_model.objects.filter(mapped_taxon__isnull=False, checklist__primary_checklist=True,
                                                  date__isnull=False).select_related('mapped_taxon'):
            taxon = record.mapped_taxon
            if taxon not in mapped_records:
                mapped_records[taxon] = set([])
            mapped_records[taxon].add(record.date)

    with transaction.atomic():
        models.Taxon.objects.all().update(first_observation_date=None, last_observation_date=None)
        for taxon in mapped_records:
            dates = sorted(mapped_records[taxon])
            if dates:
                taxon.first_observation_date = dates[0]
                taxon.last_observation_date = dates[-1]
                taxon.save()


class Command(BaseCommand):
    def handle(self, *args, **options):
        run()
