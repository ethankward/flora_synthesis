from django.core.management import BaseCommand
from django.db import transaction

from flora import models


def run():
    print('Removing orphaned checklist taxa')

    to_delete = []

    all_checklist_taxa_with_records = set([])

    with transaction.atomic():
        for record_model in [models.SEINETRecord, models.InatRecord, models.FloraRecord]:
            all_checklist_taxa_with_records.update(record_model.objects.all().values_list('checklist_taxon', flat=True))

        for checklist_taxon in models.ChecklistTaxon.objects.all():
            if checklist_taxon.pk not in all_checklist_taxa_with_records:
                to_delete.append(checklist_taxon)

        print('Deleting {} records'.format(len(to_delete)))
        for record in list(to_delete)[:10]:
            record.delete()


class Command(BaseCommand):
    def handle(self, *args, **options):
        run()
