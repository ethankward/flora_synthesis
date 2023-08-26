from django.core.management import BaseCommand

from flora import models


def get_validated_input_choices(prompt, choices):
    while True:
        value = input("{} ({}): ".format(prompt, ', '.join(choices)))
        if value in choices:
            return value


class Command(BaseCommand):

    def handle(self, *args, **options):
        print('Creating new checklist')
        result = models.Checklist()

        result.checklist_type = get_validated_input_choices("Checklist type",
                                                            models.Checklist.ChecklistTypeChoices.values)
        result.checklist_name = input("Checklist name: ")
        result.checklist_state = input("Checklist state: ")

        if result.checklist_type == models.Checklist.ChecklistTypeChoices.INAT:
            result.external_checklist_id = input("iNaturalist checklist ID: ")
        elif result.checklist_type == models.Checklist.ChecklistTypeChoices.SEINET:
            result.external_checklist_id = input("SEINet checklist ID: ")
        else:
            result.local_checklist_fn = input("Local filename: ")

        result.locality = input("Checklist locality: ")

        result.save()
