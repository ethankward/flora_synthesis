import json
import typing

from flora import models
from flora.models.records.flora_record.choices.observation_types import (
    FloraObservationTypeChoices,
)
from flora.models.taxon.choices import taxon_ranks
from flora.util import checklist_util, taxon_name_util


def get_canonical_rank(name: str) -> taxon_ranks.TaxonRankChoices:
    return taxon_name_util.TaxonName(name).rank


def get_canonical_observation_type(observation_type: str):
    for choice in FloraObservationTypeChoices:
        if choice.name.lower() == observation_type:
            return choice


class LocalFloraUpdater(checklist_util.RecordUpdater):
    def get_observation_type(self) -> FloraObservationTypeChoices:
        if self.data["observation_type"] == "True":
            return FloraObservationTypeChoices.PRESENT
        elif self.data["observation_type"] == "False":
            return FloraObservationTypeChoices.MISSING
        else:
            if self.data["observation_type"] == "P":
                return FloraObservationTypeChoices.PRESENT
            elif self.data["observation_type"] == "M":
                return FloraObservationTypeChoices.MISSING
            elif self.data["observation_type"] == "S":
                return FloraObservationTypeChoices.SUSPECTED
            else:
                return FloraObservationTypeChoices.UNKNOWN

    def update_record(self):
        if self.data is not None:
            self.record.observation_type = self.get_observation_type()
            mapped_taxon_name = self.data["mapped_taxon_name"]

            if mapped_taxon_name is not None and self.record.mapped_taxon is None:
                mapped_taxon = taxon_name_util.TaxonName(
                    mapped_taxon_name, family=self.record.checklist_taxon.family.family
                ).get_db_item()

                self.record.mapped_taxon = mapped_taxon


class LocalFloraReader(checklist_util.ChecklistReader):
    checklist_record_type = models.FloraRecord

    def __init__(self, checklist: models.Checklist):
        super().__init__(checklist)
        self.path = checklist.local_checklist_fn
        self.data = json.loads(open(self.path).read())

    def generate_data(
            self, page=None
    ) -> typing.Generator[checklist_util.ChecklistReadItem, None, None]:
        for row in self.data:
            print(row)
            external_id = row.get('external_id', None)
            checklist_taxon_name = row['checklist_taxon_name']
            checklist_family = row['checklist_taxon_family']
            observation_type = get_canonical_observation_type(row.get('observation_type', None))
            mapped_taxon_name = row.get('mapped_taxon_name', None)
            note = row.get('note', None)

            data = {
                "observation_type": observation_type,
                "mapped_taxon_name": mapped_taxon_name,
            }
            family, _ = models.ChecklistTaxonFamily.objects.get_or_create(
                checklist=self.checklist, family=checklist_family
            )
            canonical_rank = get_canonical_rank(checklist_taxon_name)
            yield checklist_util.ChecklistReadItem(
                checklist_family=family,
                taxon_name=checklist_taxon_name,
                taxon_id=external_id,
                record_id=external_id,
                observation_data=data,
                given_rank=canonical_rank.name,
                canonical_rank=canonical_rank,
                is_placeholder=True,
                note=note,
            )

    def load_checklist(self):
        self.read_all()
