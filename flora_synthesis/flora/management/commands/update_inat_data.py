from django.core.management import BaseCommand
from django.db import transaction

from flora import models


class Command(BaseCommand):
    def handle(self, *args, **options):
        for checklist in models.Checklist.objects.filter(checklist_type=models.Checklist.ChecklistTypeChoices.INAT):
            with transaction.atomic():
                checklist.update()
