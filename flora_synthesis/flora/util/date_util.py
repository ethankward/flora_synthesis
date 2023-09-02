import typing

from django.utils import timezone


def date_range_list(start_date: timezone.datetime.date,
                    end_date: timezone.datetime.date) -> typing.Generator[timezone.datetime.date, None, None]:
    curr_date = start_date
    while curr_date <= end_date:
        yield curr_date
        curr_date += timezone.timedelta(days=1)


def last_day_of_month(date: timezone.datetime) -> timezone.datetime:
    if date.month == 12:
        return date.replace(day=31)
    return date.replace(month=date.month + 1, day=1) - timezone.timedelta(days=1)


def combine_date_ranges(dates) -> typing.Generator[dict, None, None]:
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
            yield {'year': year}
            full_years.add(year)

    full_months = set([])
    for date in dates:
        if date.year not in full_years:
            if all([test_date in dates_set for test_date in date_range_list(
                    timezone.datetime(year=date.year, month=date.month, day=1).date(),
                    last_day_of_month(date)
            )]):
                yield {'year': date.year, 'month': date.month}
                full_months.add((date.year, date.month))

    for date in dates:
        if date.year not in full_years:
            if (date.year, date.month) not in full_months:
                yield {'year': date.year, 'month': date.month, 'day': date.day}
