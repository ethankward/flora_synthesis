from django.db import models
from django.db.models import Q
from django.utils import timezone


class TaxonRankChoices(models.TextChoices):
    SPECIES = 'S', 'Species'
    SUBSPECIES = 'U', 'Subspecies'
    VARIETY = 'V', 'Variety'
    HYBRID = 'H', 'Hybrid'


class ObservationTypeChoices(models.TextChoices):
    INAT_RESEARCH = 'IR', 'Research grade (iNaturalist)'
    INAT_NEEDS_ID = 'IN', 'Needs ID (iNaturalist)'
    INAT_CASUAL = 'IC', 'Casual (iNaturalist)'

    SEINET_GENERAL_RESEARCH = 'SG', 'General research (SEINet)'
    SEINET_COLLECTION = 'SC', 'Collection (SEINet)'

    BOWERS_PRESENT = 'FP', 'Bowers present in flora'
    BOWERS_MISSING = 'FM', 'Bowers missing from flora'

    UNKNOWN = 'UK', 'Unknown'


class Taxon(models.Model):
    class LifeCycleChoices(models.TextChoices):
        a = 'a', 'Annual'
        p = 'p', 'Perennial'
        u = 'u', 'Unknown'

    class IntroducedChoices(models.TextChoices):
        introduced = 'i', 'introduced'
        native = 'n', 'native'
        possibly_introduced = 'p', 'possibly introduced'

    class EndemicChoices(models.TextChoices):
        n = "n", "Not endemic"
        u = "u", "In the US only in Rincons but also occurs outside of the US"
        z = "z", "In Arizona only found in Rincons but also occurs outside of Arizona"
        a = "a", "Only found in Arizona"
        r = "r", "Only found in Rincons"

    taxon_name = models.CharField(max_length=256)

    rank = models.CharField(max_length=1, choices=TaxonRankChoices.choices)
    genus = models.CharField(max_length=256)
    family = models.CharField(max_length=256)

    parent_species = models.ForeignKey("Taxon", blank=True, null=True, on_delete=models.SET_NULL,
                                       related_name="taxon_parent_species")
    subtaxa = models.ManyToManyField("Taxon", blank=True, related_name="taxon_subtaxa")

    life_cycle = models.CharField(max_length=1, blank=True, null=True, choices=LifeCycleChoices.choices)
    introduced = models.CharField(max_length=1, choices=IntroducedChoices.choices, blank=True, null=True)
    endemic = models.CharField(max_length=1, choices=EndemicChoices.choices, blank=True, null=True)

    inat_id = models.IntegerField(blank=True, null=True)
    seinet_id = models.IntegerField(blank=True, null=True)

    on_checklists = models.ManyToManyField("Checklist", blank=True)
    observation_types = models.ManyToManyField("ObservationType", blank=True)

    class Meta:
        unique_together = [('taxon_name',)]

    def __str__(self):
        return self.taxon_name


class TaxonSynonym(models.Model):
    taxon = models.ForeignKey("Taxon", on_delete=models.CASCADE)
    synonym = models.CharField(max_length=256)

    class Meta:
        unique_together = [('synonym',)]

    def save(self, *args, **kwargs):
        from flora.util import taxon_util
        super().save(*args, **kwargs)
        to_merge = list(Taxon.objects.filter(taxon_name=self.synonym))

        for taxon in to_merge:
            if taxon != self.taxon:
                taxon_util.make_synonym_of(taxon, self.taxon)


class Checklist(models.Model):
    class ChecklistTypeChoices(models.TextChoices):
        INAT = 'i', 'iNaturalist'
        SEINET = 's', 'SEINet'
        OTHER = 'o', 'Other'

    checklist_name = models.TextField()
    checklist_type = models.CharField(max_length=1, choices=ChecklistTypeChoices.choices)
    checklist_state = models.CharField(max_length=32, blank=True, null=True)
    locality = models.TextField(blank=True, null=True)

    external_checklist_id = models.IntegerField(blank=True, null=True)
    local_checklist_fn = models.CharField(max_length=256, blank=True, null=True)

    latest_date_retrieved = models.DateField(blank=True, null=True)

    def __str__(self):
        return '{} ({})'.format(self.checklist_name, self.get_checklist_type_display())

    class Meta:
        unique_together = [('checklist_name',)]

    def update(self):
        from flora.util import seinet_util, inat_util, local_flora_util

        old_records = ChecklistRecord.objects.filter(Q(last_refreshed__isnull=True) | Q(
            last_refreshed__lt=timezone.now() - timezone.timedelta(
                days=60)), checklist=self).order_by('?')

        if self.checklist_type == self.ChecklistTypeChoices.SEINET:
            checklist_reader = seinet_util.SEINETChecklistReader(self)
            checklist_reader.read_all()
            print(old_records.count())
            records_reader = seinet_util.SEINETRecordsReader(old_records[:10])
            records_reader.read_data()

        elif self.checklist_type == self.ChecklistTypeChoices.INAT:
            inat_util.read_full_checklist(self)

            if old_records.count() > 0:
                records_reader = inat_util.InatRecordsReader(old_records)
                records_reader.read_data()
        else:
            local_flora_util.LocalFloraReader(self).read_all()

        for checklist_taxon in ChecklistTaxon.objects.filter(checklist=self):
            checklist_taxon.mapped_taxa.clear()
        for record in ChecklistRecord.objects.filter(checklist=self):
            record.save()


class ChecklistFamily(models.Model):
    family = models.CharField(max_length=256)
    checklist = models.ForeignKey("Checklist", on_delete=models.CASCADE)
    external_id = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        unique_together = [('checklist', 'family'), ('checklist', 'external_id')]
        indexes = [models.Index(fields=['family', 'checklist'])]

    def __str__(self):
        return '{}'.format(self.family)


class ChecklistTaxon(models.Model):
    checklist = models.ForeignKey("Checklist", on_delete=models.CASCADE)

    taxon_name = models.CharField(max_length=256)
    family = models.ForeignKey("ChecklistFamily", on_delete=models.CASCADE)
    genus = models.CharField(max_length=256, blank=True, null=True)

    external_id = models.IntegerField(blank=True, null=True)
    rank = models.CharField(max_length=256, blank=True, null=True)
    mapped_taxa = models.ManyToManyField("Taxon", blank=True, related_name="taxon_checklist_taxa")

    observation_types = models.ManyToManyField("ObservationType", blank=True,
                                               related_name="checklist_taxon_observation_types")

    class Meta:
        unique_together = [('checklist', 'taxon_name')]


class ObservationType(models.Model):
    observation_type = models.CharField(max_length=2, choices=ObservationTypeChoices.choices)
    observation_type_value = models.CharField(max_length=256)

    class Meta:
        unique_together = [('observation_type',)]


class ChecklistRecord(models.Model):
    checklist = models.ForeignKey("Checklist", on_delete=models.CASCADE)
    checklist_taxon = models.ForeignKey("ChecklistTaxon", on_delete=models.CASCADE)

    canonical_mapped_taxon = models.ForeignKey("Taxon", blank=True, null=True, on_delete=models.SET_NULL,
                                               related_name="taxa_checklist_appearances")

    external_record_id = models.CharField(max_length=256)

    full_metadata = models.TextField(blank=True, null=True)
    observation_type = models.ForeignKey("ObservationType", blank=True, null=True, on_delete=models.SET_NULL)

    verbatim_coordinates = models.CharField(max_length=32, blank=True, null=True)
    latitude = models.DecimalField(max_digits=32, decimal_places=12, blank=True, null=True)
    longitude = models.DecimalField(max_digits=32, decimal_places=12, blank=True, null=True)

    verbatim_date = models.CharField(max_length=32, blank=True, null=True)
    date = models.DateField(blank=True, null=True)

    verbatim_elevation = models.CharField(max_length=32, blank=True, null=True)
    elevation_ft = models.IntegerField(blank=True, null=True)

    last_refreshed = models.DateTimeField(blank=True, null=True)

    observer = models.TextField(blank=True, null=True)
    locality = models.TextField(blank=True, null=True)
    herbarium_institution = models.TextField(blank=True, null=True)

    def external_url(self):
        if self.checklist.checklist_type == Checklist.ChecklistTypeChoices.SEINET:
            return "https://swbiodiversity.org/seinet/collections/individual/index.php?occid={}".format(self.external_record_id)
        elif self.checklist.checklist_type == Checklist.ChecklistTypeChoices.INAT:
            return "https://www.inaturalist.org/observations/{}".format(self.external_record_id)

    class Meta:
        unique_together = [('checklist', 'external_record_id')]
        indexes = [models.Index(fields=['checklist', 'external_record_id'])]

    def save(self, *args, **kwargs):
        from flora.util import seinet_util, inat_util, local_flora_util

        if self.checklist.checklist_type == Checklist.ChecklistTypeChoices.INAT:
            inat_util.INatRecordUpdater(self).update_record()
        elif self.checklist.checklist_type == Checklist.ChecklistTypeChoices.SEINET:
            seinet_util.SEINETRecordUpdater(self).update_record()
        else:
            local_flora_util.LocalFloraUpdater(self).update_record()

        super().save(*args, **kwargs)


class ChecklistRecordImage(models.Model):
    class ImageSizeChoices(models.TextChoices):
        SMALL = 's', 'small'
        MEDIUM = 'm', 'medium'
        LARGE = 'l', 'large'

    checklist_record = models.ForeignKey("ChecklistRecord", on_delete=models.CASCADE,
                                         related_name="checklist_record_images")
    image_url = models.URLField()
    image_size = models.CharField(max_length=1, choices=ImageSizeChoices.choices, blank=True, null=True)
