from django.core.management import BaseCommand

from flora.management.commands import (
    update_inat_data,
    update_seinet_data,
    update_observation_dates,
)


def run():
    print("Updating inat data")
    update_inat_data.run()
    print("Updating seinet data")
    update_seinet_data.run()
    print("Updating observation dates")
    update_observation_dates.run()


class Command(BaseCommand):
    def handle(self, *args, **options):
        run()
