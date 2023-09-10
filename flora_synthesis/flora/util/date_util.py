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
            created_d1 = "{}-01-01".format(year)
            created_d2 = "{}-12-31".format(year)
            end_date = timezone.datetime(year=year, month=12, day=31)
            yield {'created_d1': created_d1, 'created_d2': created_d2}, end_date
            full_years.add(year)

    full_months = set([])
    for date in dates:
        last_month_day = last_day_of_month(date)
        if date.year not in full_years:
            if all([test_date in dates_set for test_date in date_range_list(
                    timezone.datetime(year=date.year, month=date.month, day=1).date(),
                    last_month_day
            )]):
                if (date.year, date.month) not in full_months:
                    created_d1 = "{}-{}-01".format(date.year, date.month)
                    created_d2 = "{}-{}-{}".format(date.year, date.month, last_month_day.day)
                    end_date = timezone.datetime(year=date.year, month=date.month, day=last_month_day.day)
                    yield {'created_d1': created_d1, 'created_d2': created_d2}, end_date
                    full_months.add((date.year, date.month))

    for date in dates:
        if date.year not in full_years:
            if (date.year, date.month) not in full_months:
                end_date = timezone.datetime(year=date.year, month=date.month, day=date.day)
                yield {'created_on': "{}-{}-{}".format(date.year, date.month, date.day)}, end_date
