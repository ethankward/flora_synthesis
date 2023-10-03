from django.test import TestCase
from django.utils import timezone

from flora.util import date_util


class DateUtilNameTests(TestCase):
    def test_basic(self):
        """Test date interval generation."""
        start_date = timezone.datetime(year=2020, month=1, day=1).date()
        end_date = timezone.datetime(year=2023, month=8, day=5).date()

        t1 = [
            {"created_d1": "2020-01-01", "created_d2": "2020-12-31"},
            {"created_d1": "2021-01-01", "created_d2": "2021-12-31"},
            {"created_d1": "2022-01-01", "created_d2": "2022-12-31"},
            {"created_d1": "2023-1-01", "created_d2": "2023-1-31"},
            {"created_d1": "2023-2-01", "created_d2": "2023-2-28"},
            {"created_d1": "2023-3-01", "created_d2": "2023-3-31"},
            {"created_d1": "2023-4-01", "created_d2": "2023-4-30"},
            {"created_d1": "2023-5-01", "created_d2": "2023-5-31"},
            {"created_d1": "2023-6-01", "created_d2": "2023-6-30"},
            {"created_d1": "2023-7-01", "created_d2": "2023-7-31"},
            {"created_on": "2023-8-1"},
            {"created_on": "2023-8-2"},
            {"created_on": "2023-8-3"},
            {"created_on": "2023-8-4"},
            {"created_on": "2023-8-5"},
        ]

        t2 = list(
            date_util.combine_date_ranges(
                list(date_util.date_range_list(start_date, end_date))
            )
        )
        t2 = [i[0] for i in t2]

        self.assertListEqual(t1, t2)
