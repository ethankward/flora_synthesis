import json
import typing

from django.utils import timezone

from flora import models
from flora.models.records.inat_record.util import inat_api
from flora.models.records.util import record_reader
from flora.util import http_util

SESSION = http_util.get_session()


class InatRecordsReader(record_reader.RecordReader):
    def __init__(self, records: typing.List[models.InatRecord]):
        super().__init__(records)
        self.records_dict = {str(record.external_id): record for record in self.records}
        self.inat_api = inat_api.InatApi(session=SESSION)

    def read_records(self):
        if len(self.records) == 0:
            return
        observation_ids = [r.external_id for r in self.records]
        print(observation_ids)
        for observation_data_item in self.inat_api.read_observation_data({}, observation_ids):
            record = self.records_dict[str(observation_data_item['id'])]
            record.full_metadata = json.dumps(observation_data_item)
            record.last_refreshed = timezone.now()
            record.save()
