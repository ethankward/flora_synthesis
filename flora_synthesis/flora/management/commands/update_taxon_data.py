from django.core.management import BaseCommand
from django.db import transaction

from flora import models


def update_on_checklists():
    for taxon in models.Taxon.objects.all():
        checklists = set([])
        for appearance in taxon.taxa_checklist_appearances.all():
            checklists.add(appearance.checklist)
        taxon.on_checklists.clear()
        taxon.on_checklists.add(*checklists)


def update_observation_types():
    for taxon in models.Taxon.objects.all():
        taxon.observation_types.clear()
        for appearance in taxon.taxa_checklist_appearances.all():
            if appearance.observation_type is not None:
                taxon.observation_types.add(appearance.observation_type)

    for checklist_taxon in models.ChecklistTaxon.objects.all():
        checklist_taxon.observation_types.clear()
        for record in models.ChecklistRecord.objects.filter(checklist_taxon=checklist_taxon):
            checklist_taxon.observation_types.add(record.observation_type)


class Command(BaseCommand):
    def handle(self, *args, **options):
        with transaction.atomic():
            update_on_checklists()
            update_observation_types()
