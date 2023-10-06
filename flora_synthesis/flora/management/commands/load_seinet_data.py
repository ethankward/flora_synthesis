"""
Load data for a SEINet checklist.
"""
from django.core.management import BaseCommand
from django.db import transaction

from flora import models
from flora.models.checklist.choices import checklist_types


def run():
    for checklist in models.Checklist.objects.filter(
            checklist_type=checklist_types.ChecklistTypeChoices.SEINET
    ):
        print(checklist)
        with transaction.atomic():
            checklist.load()


class Command(BaseCommand):
    def handle(self, *args, **options):
        run()
