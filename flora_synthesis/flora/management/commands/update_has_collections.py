from django.core.management import BaseCommand
from django.db import transaction

from flora import models
from flora.models.records.seinet_record.choices import observation_types


def run():
    print('Updating collection statuses')
    taxa_with_collections = set([])
    record_models = [models.SEINETRecord]
    for record_model in record_models:
        for record in record_model.objects.filter(mapped_taxon__isnull=False,
                                                  checklist__primary_checklist=True,
                                                  observation_type=observation_types.SEINETObservationTypeChoices.COLLECTION).select_related(
            'mapped_taxon',
            'mapped_taxon__parent_species'):
            taxon = record.mapped_taxon
            taxa_with_collections.add(taxon.pk)

            parent_taxon = taxon.parent_species
            if parent_taxon is not None:
                taxa_with_collections.add(parent_taxon.pk)

    print('{} taxa with collections'.format(len(taxa_with_collections)))

    with transaction.atomic():
        models.Taxon.objects.all().update(has_collections=False)
        models.Taxon.objects.filter(pk__in=taxa_with_collections).update(has_collections=True)

    print('Finished update')


class Command(BaseCommand):
    def handle(self, *args, **options):
        run()
