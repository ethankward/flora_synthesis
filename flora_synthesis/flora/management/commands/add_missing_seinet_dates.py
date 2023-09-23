import datetime
import webbrowser

from django.core.management import BaseCommand

from flora import models
from flora.models.records.seinet_record.choices.observation_types import SEINETObservationTypeChoices


def run():
    missing_date_records = models.SEINETRecord.objects.filter(date__isnull=True).exclude(
        observation_type=SEINETObservationTypeChoices.NOTE_PLACEHOLDER).exclude(unknown_date=True)
    print('Records with missing dates: {}'.format(missing_date_records.count()))

    for record in missing_date_records:
        url = record.external_url()
        if url is None:
            print('No URL: {}'.format(record.id))
            continue
        webbrowser.open(url, new=True)
        print(
            'No date known: {}'.format(record.external_id))
        year = int(input("Year: "))
        if year == -1:
            record.unknown_date = True
            record.save()
        else:
            month = int(input("Month: "))
            day = int(input("Day: "))
            date = datetime.datetime(year=year, month=month, day=day)
            record.date = date
            record.save()


class Command(BaseCommand):
    def handle(self, *args, **options):
        run()
