import typing

from flora import models


class RecordReader:
    def __init__(self, records: typing.List[models.Record]):
        self.records = records

    def read_records(self):
        pass
