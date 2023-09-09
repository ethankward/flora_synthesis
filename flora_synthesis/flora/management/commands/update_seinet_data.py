from django.core.management import BaseCommand
from django.db import transaction

from flora import models
from flora.models.checklist.choices import checklist_types
from flora.util import seinet_util


class Command(BaseCommand):
    def handle(self, *args, **options):
        for checklist in models.Checklist.objects.filter(checklist_type=checklist_types.ChecklistTypeChoices.SEINET):
            print(checklist)
            with transaction.atomic():
                checklist.load()
                seinet_util.SEINETRecordReader(checklist).read_records(limit=10)

                for record in models.SEINETRecord.objects.filter(checklist_taxon__checklist=checklist):
                    record.save()
