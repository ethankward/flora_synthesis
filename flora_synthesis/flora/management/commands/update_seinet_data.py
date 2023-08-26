from django.core.management import BaseCommand

from flora import models
from django.db import transaction


class Command(BaseCommand):
    def handle(self, *args, **options):
        for checklist in models.Checklist.objects.filter(checklist_type=models.Checklist.ChecklistTypeChoices.SEINET):
            with transaction.atomic():
                checklist.update()
