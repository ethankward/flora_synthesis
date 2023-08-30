class RecordUpdater:
    def __init__(self, record):
        self.record = record
        self.data = self.record.load_data()

    def update_record(self):
        pass
