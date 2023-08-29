from django.core.management import BaseCommand
from django.db import transaction

from flora import models


class Command(BaseCommand):
    def handle(self, *args, **options):
        with transaction.atomic():
            for checklist_record in models.ChecklistRecord.objects.all():
                checklist_record.save()
            for checklist_taxon in models.ChecklistTaxon.objects.all():
                checklist_taxon.save()
