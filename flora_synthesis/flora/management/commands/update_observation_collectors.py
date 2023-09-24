from django.core.management import BaseCommand
from django.db import transaction

from flora import models


def split_observer_str(observer_str):
    delimiters = [', ', ' & ', ' and ', '|', '; ']

    for delimiter in delimiters:
        if delimiter in observer_str:
            return observer_str.split(delimiter)

    return [observer_str]


def get_canonical_name(name):
    return name.replace(' ', '').replace('.', '').lower()


def get_match(name, all_aliases):
    for alias in all_aliases:
        if get_canonical_name(alias.alias) == get_canonical_name(name):
            return alias.collector


def get_matches(observer_str, all_aliases):
    names = split_observer_str(observer_str)

    for name in names:
        match = get_match(name, all_aliases)
        if match is not None:
            yield match


def run():
    all_aliases = list(models.CollectorAlias.objects.all().select_related('collector'))

    collector_dates = {}

    with transaction.atomic():
        for seinet_record in models.SEINETRecord.objects.filter(observer__isnull=False, active=True):
            seinet_record.collectors.clear()

            observer_str = seinet_record.observer

            for collector in get_matches(observer_str, all_aliases):
                seinet_record.collectors.add(collector)
                print(seinet_record, collector)
                if collector not in collector_dates:
                    collector_dates[collector] = []
                if seinet_record.date is not None:
                    collector_dates[collector].append(seinet_record.date)

        models.Collector.objects.update(first_collection_year=None, last_collection_year=None)
        for collector in collector_dates:

            if collector_dates[collector]:

                dates = sorted(collector_dates[collector])
                first_year = dates[0].year
                last_year = dates[-1].year

                collector.first_collection_year = first_year
                collector.last_collection_year = last_year
                collector.save()


class Command(BaseCommand):
    def handle(self, *args, **options):
        run()
