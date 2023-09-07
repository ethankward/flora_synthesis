from django.core.management import BaseCommand
from django.db import transaction

from flora import models


class Command(BaseCommand):
    def handle(self, *args, **options):
        with transaction.atomic():
            models.ObservationDate.objects.all().delete()
            for checklist in models.Checklist.objects.filter(primary_checklist=True):
                for inat_record in models.InatRecord.objects.filter(
                        checklist_taxon__checklist=checklist).select_related('mapped_taxon'):
                    if inat_record.date is not None and inat_record.mapped_taxon is not None:
                        taxon = inat_record.mapped_taxon
                        observation_date = models.ObservationDate.objects.create(date=inat_record.date,
                                                                                 url=inat_record.external_url())
                        taxon.observation_dates.add(observation_date)

                for seinet_record in models.SEINETRecord.objects.filter(
                        checklist_taxon__checklist=checklist).select_related('mapped_taxon'):
                    if seinet_record.date is not None and seinet_record.mapped_taxon is not None:
                        taxon = seinet_record.mapped_taxon
                        observation_date = models.ObservationDate.objects.create(date=seinet_record.date,
                                                                                 url=seinet_record.external_url())
                        taxon.observation_dates.add(observation_date)

                for taxon in models.Taxon.objects.all():
                    observation_dates = sorted(taxon.observation_dates.all(), key=lambda x: x.date)
                    if observation_dates:
                        taxon.first_observation_date = observation_dates[0]
                        taxon.last_observation_date = observation_dates[-1]
                        taxon.save()
