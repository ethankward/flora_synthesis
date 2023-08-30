from django.utils import timezone

from flora import models
from flora.models.checklist.choices import checklist_types
from flora.models.checklist.util import missing_dates
from flora.models.records.flora_record.util import read_flora_checklist
from flora.models.records.inat_record.util import read_inat_checklist
from flora.models.records.seinet_record.util import read_seinet_checklist


def load_checklist(checklist: models.Checklist):
    if checklist.checklist_type == checklist_types.ChecklistTypeChoices.SEINET:
        models.SEINETRecord.objects.filter(checklist_taxon__checklist=checklist).update(active=False)
        generator = read_seinet_checklist.SEINETChecklistReader(checklist)
        generator.read_all(reactivate=True)

    elif checklist.checklist_type == checklist_types.ChecklistTypeChoices.INAT:
        years_to_update, months_to_update, dates_to_update = missing_dates.missing_dates(checklist)

        for year in years_to_update:
            print('Updating year {}'.format(year))
            generator = read_inat_checklist.InatChecklistReader(checklist, {'year': year})
            generator.read_all()
        for year, month in months_to_update:
            print('Updating year {} month {}'.format(year, month))
            generator = read_inat_checklist.InatChecklistReader(checklist, {'year': year, 'month': month})
            generator.read_all()
        for date in dates_to_update:
            print('Updating {}'.format(date))
            generator = read_inat_checklist.InatChecklistReader(checklist, {'year': date.year, 'month': date.month,
                                                                            'day': date.day})
            generator.read_all()

        checklist.latest_date_retrieved = timezone.now().date() - timezone.timedelta(days=2)
        checklist.save()

    else:
        generator = read_flora_checklist.LocalFloraReader(checklist)
        generator.read_all()
