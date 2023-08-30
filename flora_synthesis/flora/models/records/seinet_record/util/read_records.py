from flora.util import http_util
from models.records.util import record_reader

SESSION = http_util.get_session()


class SEINETRecordReader(record_reader.RecordReader):
    def read_records(self):
        for record in self.records:
            url = "https://swbiodiversity.org/seinet/collections/individual/index.php?occid={}".format(
                record.external_id)
            record.full_metadata = SESSION.get(url).text
            record.save()
