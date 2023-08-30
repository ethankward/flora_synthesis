from flora import models


class RecordUpdater:
    def __init__(self, record: models.Record):
        self.record = record
        self.data = self.record.load_data()

    def update_record(self):
        pass
