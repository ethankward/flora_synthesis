from django.test import TestCase
from django.utils import timezone

from flora.util import date_util


class DateUtilNameTests(TestCase):
    def test_basic(self):
        start_date = timezone.datetime(year=2020, month=1, day=1).date()
        end_date = timezone.datetime(year=2023, month=8, day=5).date()

        t1 = [{'year': 2020}, {'year': 2021}, {'year': 2022}, {'year': 2023, 'month': 1}, {'year': 2023, 'month': 2},
              {'year': 2023, 'month': 3}, {'year': 2023, 'month': 4}, {'year': 2023, 'month': 5},
              {'year': 2023, 'month': 6}, {'year': 2023, 'month': 7}, {'year': 2023, 'month': 8, 'day': 1},
              {'year': 2023, 'month': 8, 'day': 2}, {'year': 2023, 'month': 8, 'day': 3},
              {'year': 2023, 'month': 8, 'day': 4}, {'year': 2023, 'month': 8, 'day': 5}]
        t2 = list(date_util.combine_date_ranges(list(date_util.date_range_list(start_date, end_date))))

        self.assertListEqual(t1, t2)
