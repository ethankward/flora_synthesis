import json
import typing
from dataclasses import dataclass

from flora import models


@dataclass
class ChecklistReadItem:
    checklist_family: str
    taxon_name: str
    taxon_id: str
    record_id: typing.Optional[str]
    observation_data: typing.Optional[dict]
    given_rank: str
    is_placeholder: bool = False


class ChecklistReader:
    checklist_record_type = models.Record

    def __init__(self, checklist, parameters=None):
        self.checklist = checklist
        self.parameters = parameters

    def generate_data(self) -> typing.Generator[ChecklistReadItem, None, None]:
        pass

    def read_all(self, reactivate=False):
        for checklist_read_item in self.generate_data():

            checklist_taxon, _ = models.ChecklistTaxon.objects.get_or_create(
                checklist=self.checklist,
                taxon_name=checklist_read_item.taxon_name,
                family=checklist_read_item.checklist_family
            )

            checklist_taxon.family = checklist_read_item.checklist_family
            checklist_taxon.genus = checklist_read_item.taxon_name.split(' ')[0]
            checklist_taxon.external_id = checklist_read_item.taxon_id
            checklist_taxon.rank = checklist_read_item.given_rank
            checklist_taxon.save()

            try:
                checklist_record = self.checklist_record_type.objects.get(
                    external_id=checklist_read_item.record_id,
                )
            except self.checklist_record_type.DoesNotExist:
                checklist_record = self.checklist_record_type(
                    external_id=checklist_read_item.record_id,
                )

            if reactivate:
                checklist_record.active = True

            checklist_record.checklist_taxon = checklist_taxon
            checklist_record.is_placeholder = checklist_read_item.is_placeholder

            if checklist_read_item.observation_data is not None:
                checklist_record.full_metadata = json.dumps(checklist_read_item.observation_data)

            checklist_record.save()
