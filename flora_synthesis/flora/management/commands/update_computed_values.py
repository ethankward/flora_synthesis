"""
Update database values that are not automatically kept up to date.
"""
from django.conf import settings
from django.core.management import BaseCommand
from django_q.tasks import async_task
from rest_framework import status
from rest_framework.response import Response

from flora.management.commands import remove_orphan_checklist_taxa, update_has_collections, \
    update_observation_collectors, update_observation_dates


def run():
    tasks = [
        remove_orphan_checklist_taxa.run,
        update_has_collections.run,
        update_observation_collectors.run,
        update_observation_dates.run,
    ]
    for task in tasks:
        if settings.PRODUCTION:
            async_task(task)
        else:
            task()

    return Response(status=status.HTTP_200_OK)


class Command(BaseCommand):
    def handle(self, *args, **options):
        run()
