from django.core.management import BaseCommand

from flora import models
from flora.models.checklist.choices import checklist_types
from flora.util import inat_util


def import_inat_obs(checklist, observation_id):
    reader = inat_util.InatChecklistReader(checklist=checklist)
    reader.load_specific_observations([observation_id])


class Command(BaseCommand):
    def handle(self, *args, **options):
        checklists = list(models.Checklist.objects.filter(checklist_type=checklist_types.ChecklistTypeChoices.INAT))

        if len(checklists) == 1:
            checklist = checklists[0]
        else:
            print('Checklists:')
            for i, checklist in enumerate(checklists):
                print('\t{}: {}'.format(i, checklist.checklist_name))
            checklist = checklists[int(input("Choose checklist: "))]

        url = input("Observation url: ")
        if url.endswith('/'):
            url = url[:-1]

        observation_id = int(url.split('/')[-1])

        import_inat_obs(checklist, observation_id)
