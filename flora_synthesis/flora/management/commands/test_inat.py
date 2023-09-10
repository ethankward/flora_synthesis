from django.core.management import BaseCommand

from flora import models
from flora.util import http_util
from flora.util import inat_util

SESSION = http_util.get_session()


def run():
    ch = models.Checklist.objects.get(checklist_name="iNaturalist Rincons")
    parameters = {'place_id': ch.external_checklist_id, 'taxon_id': 211194, 'per_page': 200,
                  'created_d1': '2019-01-01', 'created_d2': '2019-12-31'}

    inat_api = inat_util.InatApi(session=SESSION)
    for observation_data_item in inat_api.read_observation_data(parameters):
        print(observation_data_item['id'])
        if observation_data_item['observed_on'] is None:
            print('here', observation_data_item['id'])
            input()


class Command(BaseCommand):
    def handle(self, *args, **options):
        run()
