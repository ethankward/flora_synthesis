from django.core.management import BaseCommand
from django.db import transaction

from flora import models
from flora.models.checklist.choices import checklist_types


class Command(BaseCommand):
    def handle(self, *args, **options):
        for checklist in models.Checklist.objects.filter(checklist_type=checklist_types.ChecklistTypeChoices.FLORA):
            with transaction.atomic():
                checklist.load()
