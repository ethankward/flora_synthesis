import json
import typing
from dataclasses import dataclass

from django.utils import timezone

from flora import models
from flora.models.taxon.choices import taxon_ranks
from flora.util import taxon_name_util
from flora.models.checklist.choices.checklist_types import ChecklistTypeChoices


@dataclass
class ChecklistReadItem:
    checklist_family: str
    taxon_name: str
    taxon_id: str
    record_id: typing.Optional[str]
    observation_data: typing.Optional[dict]
    given_rank: str
    canonical_rank: taxon_ranks.TaxonRankChoices
    is_placeholder: bool = False
    note: str = None


class ChecklistReader:
    checklist_record_type = models.Record

    def __init__(self, checklist: models.Checklist):
        self.checklist = checklist
        self.parameters = {}

    def generate_data(
        self, page=None
    ) -> typing.Generator[ChecklistReadItem, None, None]:
        pass

    def read_all(self, reactivate: bool = False, page=None):
        for checklist_read_item in self.generate_data(page=page):

            checklist_taxon: models.ChecklistTaxon
            checklist_taxon, _ = models.ChecklistTaxon.objects.get_or_create(
                checklist=self.checklist,
                taxon_name=checklist_read_item.taxon_name,
                family=checklist_read_item.checklist_family,
            )

            checklist_taxon.family = checklist_read_item.checklist_family
            checklist_taxon.genus = checklist_read_item.taxon_name.split(" ")[0]
            checklist_taxon.external_id = checklist_read_item.taxon_id
            checklist_taxon.rank = checklist_read_item.given_rank
            checklist_taxon.save()

            try:
                checklist_record = self.checklist_record_type.objects.get(
                    external_id=checklist_read_item.record_id, checklist=self.checklist
                )
            except self.checklist_record_type.DoesNotExist:
                checklist_record = self.checklist_record_type(
                    external_id=checklist_read_item.record_id, checklist=self.checklist
                )

            if reactivate:
                checklist_record.active = True

            checklist_record.checklist_taxon = checklist_taxon
            checklist_record.is_placeholder = checklist_read_item.is_placeholder

            if checklist_read_item.observation_data is not None:
                checklist_record.full_metadata = json.dumps(
                    checklist_read_item.observation_data
                )
                checklist_record.last_refreshed = timezone.now()

            checklist_record.save()

            if checklist_record.mapped_taxon is None or (
                self.checklist.checklist_type != ChecklistTypeChoices.FLORA
            ):
                mapped_taxon = taxon_name_util.TaxonName(
                    checklist_taxon.taxon_name,
                    family=checklist_taxon.family.family,
                    given_rank=checklist_read_item.canonical_rank,
                ).get_db_item()

                checklist_record.mapped_taxon = mapped_taxon
                checklist_record.save()

            if checklist_read_item.note is not None:
                checklist_record_note = models.ChecklistRecordNote(
                    note=checklist_read_item.note
                )
                checklist_record_note.save()
                checklist_record.notes.add(checklist_record_note)

            checklist_taxon.save()

    def load_checklist(self):
        pass


class RecordReader:
    def __init__(self, checklist: models.Checklist):
        self.checklist = checklist

    def read_records(
        self,
        records: typing.Optional[typing.List[models.Record]] = None,
        limit: int = 10,
    ):
        pass


class RecordUpdater:
    def __init__(self, record: models.Record):
        self.record = record
        self.data = self.record.load_data()

    def update_record(self):
        pass
