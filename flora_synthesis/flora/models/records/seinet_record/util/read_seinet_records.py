from django.utils import timezone

from flora.models.records.util import record_reader
from flora.util import http_util

SESSION = http_util.get_session()


class SEINETRecordReader(record_reader.RecordReader):
    def read_records(self):
        for record in self.records:
            url = "https://swbiodiversity.org/seinet/collections/individual/index.php?occid={}".format(
                record.external_id)
            record.full_metadata = SESSION.get(url).text
            record.last_refreshed = timezone.now()
            record.save()
