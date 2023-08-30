from django.utils import timezone

from flora.util import date_util


def missing_dates(checklist):
    if checklist.latest_date_retrieved is not None:
        start_date = checklist.latest_date_retrieved
    elif checklist.earliest_year is not None:
        start_date = timezone.datetime(year=checklist.earliest_year, month=1, day=1).date()
    else:
        return

    end_date = timezone.now().date() - timezone.timedelta(days=2)
    years, months, dates = date_util.combine_date_ranges(
        list(date_util.date_range_list(start_date, end_date)))
    return years, months, dates
