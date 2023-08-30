from flora import models
from flora.models.checklist.choices import checklist_types
from flora.models.records.flora_record.util import read_flora_checklist
from flora.models.records.inat_record.util import read_inat_checklist
from flora.models.records.seinet_record.util import read_seinet_checklist


def load_checklist(checklist: models.Checklist):
    if checklist.checklist_type == checklist_types.ChecklistTypeChoices.SEINET:
        generator = read_seinet_checklist.SEINETChecklistReader(checklist)
    elif checklist.checklist_type == checklist_types.ChecklistTypeChoices.INAT:
        generator = read_inat_checklist.InatChecklistReader(checklist, {'year': 2023})
    else:
        generator = read_flora_checklist.LocalFloraReader(checklist)

    for read_item in generator.generate_data():
        print(read_item.taxon_name)
