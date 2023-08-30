import json
import typing

from flora import models
from flora.util import http_util
from models.records.util import record_reader
from models.records.inat_record.util import inat_api

SESSION = http_util.get_session()


class InatRecordsReader(record_reader.RecordReader):
    def __init__(self, checklist_records: typing.List[models.InatRecord]):
        super().__init__(checklist_records)
        self.records_dict = {record.external_id: record for record in self.records}
        self.inat_api = inat_api.InatApi(session=SESSION)

    def read_records(self):
        observation_ids = [r.external_id for r in self.records]
        for observation_data_item in self.inat_api.read_observation_data({}, observation_ids):
            record = self.records_dict[str(observation_data_item['id'])]
            record.full_metadata = json.dumps(observation_data_item)
            record.save()
