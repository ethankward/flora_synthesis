from django.core.management import BaseCommand
from django.db import transaction

from flora import models
from flora.models.checklist.choices import checklist_types
from flora.models.checklist.util import load_checklist


class Command(BaseCommand):
    def handle(self, *args, **options):
        for checklist in models.Checklist.objects.filter(checklist_type=checklist_types.ChecklistTypeChoices.SEINET):
            with transaction.atomic():
                load_checklist.load_checklist(checklist)
