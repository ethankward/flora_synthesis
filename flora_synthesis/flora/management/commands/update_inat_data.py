from django.core.management import BaseCommand
from django.db import transaction

from flora import models
from flora.models.checklist.choices import checklist_types
from flora.util import inat_util


def run():
    for checklist in models.Checklist.objects.filter(checklist_type=checklist_types.ChecklistTypeChoices.INAT):
        checklist.load()
        inat_util.InatRecordsReader(checklist).read_records(limit=10)

        with transaction.atomic():
            for record in models.InatRecord.objects.filter(checklist_taxon__checklist=checklist):
                record.save()


class Command(BaseCommand):
    def handle(self, *args, **options):
        run()
