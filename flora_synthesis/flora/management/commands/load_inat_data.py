"""
Load data for iNaturalist checklist.
"""
from django.core.management import BaseCommand

from flora import models
from flora.models.checklist.choices import checklist_types


def run():
    for checklist in models.Checklist.objects.filter(
            checklist_type=checklist_types.ChecklistTypeChoices.INAT
    ):
        checklist.load()


class Command(BaseCommand):
    def handle(self, *args, **options):
        run()
