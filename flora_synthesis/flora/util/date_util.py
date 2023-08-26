from django.utils import timezone


def date_range_list(start_date, end_date):
    curr_date = start_date
    while curr_date <= end_date:
        yield curr_date
        curr_date += timezone.timedelta(days=1)


def last_day_of_month(date):
    if date.month == 12:
        return date.replace(day=31)
    return date.replace(month=date.month + 1, day=1) - timezone.timedelta(days=1)


def combine_date_ranges(dates):
    years = set([])

    for date in dates:
        years.add(date.year)

    years = sorted(years)
    dates_set = set(dates)

    full_years = set([])

    for year in years:
        if all([test_date in dates_set for test_date in
                date_range_list(timezone.datetime(year=year, month=1, day=1).date(),
                                timezone.datetime(year=year, month=12, day=31).date())]):
            full_years.add(year)

    full_months = set([])
    for date in dates:
        if date.year not in full_years:

            if all([test_date in dates_set for test_date in date_range_list(
                    timezone.datetime(year=date.year, month=date.month, day=1).date(),
                    last_day_of_month(date)
            )]):
                full_months.add((date.year, date.month))

    remaining_dates = set([])
    for date in dates:
        if date.year not in full_years:
            if (date.year, date.month) not in full_months:
                remaining_dates.add(date)

    return sorted(full_years), sorted(full_months), sorted(remaining_dates)
