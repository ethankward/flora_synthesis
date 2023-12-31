"""
Load data from a local flora checklist.
"""
from django.core.management import BaseCommand
from django.db import transaction

from flora import models
from flora.models.checklist.choices import checklist_types


def run():
    for checklist in models.Checklist.objects.filter(
        checklist_type=checklist_types.ChecklistTypeChoices.FLORA
    ):
        print(checklist.checklist_name)
        with transaction.atomic():
            checklist.load()


class Command(BaseCommand):
    def handle(self, *args, **options):
        run()
