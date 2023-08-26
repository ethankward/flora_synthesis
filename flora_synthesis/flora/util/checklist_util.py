import json
import typing

from django.utils import timezone

from flora import models
from flora.util import taxon_util


class ChecklistReader:
    def __init__(self, checklist, parameters=None):
        self.checklist = checklist
        self.parameters = parameters

    def generate_data(self) -> typing.Generator:
        # checklist_family, taxon_name, taxon_id, record_id, observation_data, given_rank
        pass

    def read_all(self):
        for checklist_family, taxon_name, taxon_id, record_id, observation_data, given_rank in self.generate_data():

            checklist_taxon, _ = models.ChecklistTaxon.objects.get_or_create(
                checklist=self.checklist,
                taxon_name=taxon_name,
                family=checklist_family
            )

            checklist_taxon.family = checklist_family
            checklist_taxon.genus = taxon_name.split(' ')[0]
            checklist_taxon.external_id = taxon_id
            checklist_taxon.rank = given_rank
            checklist_taxon.save()

            try:
                checklist_record = models.ChecklistRecord.objects.get(
                    external_record_id=record_id,
                    checklist=self.checklist,
                )
            except models.ChecklistRecord.DoesNotExist:
                checklist_record = models.ChecklistRecord(
                    external_record_id=record_id,
                    checklist=self.checklist,
                )

            checklist_record.checklist_taxon = checklist_taxon

            if observation_data is not None:
                checklist_record.full_metadata = json.dumps(observation_data)
            checklist_record.save()


class RecordsReader:
    def __init__(self, checklist_records):
        self.checklist_records = checklist_records

    def read_data(self):
        pass


class IndividualRecordUpdater:
    def __init__(self, checklist_record):
        self.checklist_record = checklist_record

    def get_observation_type(self):
        pass

    def get_herbarium_institution(self):
        pass

    def get_verbatim_date(self):
        pass

    def get_date(self):
        pass

    def get_verbatim_coordinates(self):
        pass

    def get_coordinates(self):
        return None, None

    def get_verbatim_elevation(self):
        pass

    def get_observer(self):
        pass

    def get_locality(self):
        pass

    def get_image_urls(self):
        yield from ()

    def get_canonical_rank(self, taxon_name, rank):
        return

    def get_mapped_taxon(self, name, family, rank):
        return taxon_util.TaxonName(name, family=family, given_rank=rank).get_db_item()

    def update_record(self):
        record = self.checklist_record

        if self.checklist_record.full_metadata is not None:
            record.observation_type = self.get_observation_type()
            record.herbarium_institution = self.get_herbarium_institution()
            record.verbatim_date = self.get_verbatim_date()
            record.date = self.get_date()
            record.verbatim_coordinates = self.get_verbatim_coordinates()
            record.latitude, record.longitude = self.get_coordinates()
            record.verbatim_elevation = self.get_verbatim_elevation()
            record.observer = self.get_observer()
            record.locality = self.get_locality()
            record.last_refreshed = timezone.now()

        if record.pk is not None:
            checklist_taxon = record.checklist_taxon

            if record.canonical_mapped_taxon is None:
                rank = self.get_canonical_rank(checklist_taxon.taxon_name, checklist_taxon.rank)
                mapped_taxon = self.get_mapped_taxon(checklist_taxon.taxon_name, checklist_taxon.family.family,
                                                     rank)
                record.canonical_mapped_taxon = mapped_taxon

            if record.canonical_mapped_taxon is not None:
                db_taxon = record.canonical_mapped_taxon

                checklist_taxon.mapped_taxa.add(db_taxon)

                parent = db_taxon.parent_species
                if parent is not None:
                    checklist_taxon.mapped_taxa.add(parent)

                if checklist_taxon.external_id is not None:
                    checklist = checklist_taxon.checklist
                    if checklist.checklist_type == models.Checklist.ChecklistTypeChoices.SEINET:
                        db_taxon.seinet_id = checklist_taxon.external_id
                    elif checklist.checklist_type == models.Checklist.ChecklistTypeChoices.INAT:
                        db_taxon.inat_id = checklist_taxon.external_id
                    db_taxon.save()

            models.ChecklistRecordImage.objects.filter(checklist_record=record).delete()
            for image_url, size in self.get_image_urls():
                models.ChecklistRecordImage.objects.create(checklist_record=record, image_url=image_url,
                                                           image_size=size)
