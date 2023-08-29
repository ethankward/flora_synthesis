import itertools
import json
import typing

from django.utils import timezone

from flora import models
from flora.util import http_util, checklist_util, date_util

SESSION = http_util.get_session()


def read_api_data(url, parameters, paginate=True):
    print(url, parameters)
    if not paginate:
        data = json.loads(SESSION.get(url, params={**parameters}).text)
        results = data['results']
        yield from results
    else:
        for page in itertools.count(1):
            data = json.loads(SESSION.get(url, params={**parameters, **{'page': page}}).text)
            results = data['results']
            if len(results) == 0:
                break
            yield from results


def get_urls_with_ids(base_url, ids=None):
    if ids is None:
        yield base_url
    else:
        size = 30

        for i in range(len(ids)//size + 1):
            taxon_ids_comma_delimited = ','.join(map(str, ids[size*i:size*(i + 1)]))
            url = base_url + '/' + taxon_ids_comma_delimited
            yield url


def read_taxon_data(taxon_ids):
    base_url = "https://api.inaturalist.org/v1/taxa"
    for url in get_urls_with_ids(base_url, taxon_ids):
        yield from read_api_data(url, {}, paginate=False)


def read_observation_data(parameters, observation_ids=None):
    base_url = "https://api.inaturalist.org/v1/observations"
    for url in get_urls_with_ids(base_url, observation_ids):
        yield from read_api_data(url, parameters)


class InatRecordsReader(checklist_util.RecordsReader):
    def __init__(self, checklist_records):
        super().__init__(checklist_records)
        self.records_dict = {record.external_record_id: record for record in self.checklist_records}

    def read_data(self):
        observation_ids = [r.external_record_id for r in self.checklist_records]
        for observation_data_item in read_observation_data({}, observation_ids):
            record = self.records_dict[str(observation_data_item['id'])]
            record.full_metadata = json.dumps(observation_data_item)
            record.save()


class INatRecordUpdater(checklist_util.IndividualRecordUpdater):
    def __init__(self, checklist_record):
        super().__init__(checklist_record)
        if checklist_record.full_metadata is not None:
            self.metadata = json.loads(checklist_record.full_metadata)
        else:
            self.metadata = None

    def get_observation_type(self):
        quality_grade = self.metadata['quality_grade']

        if quality_grade == 'research':
            observation_type = models.ObservationTypeChoices.INAT_RESEARCH
        elif quality_grade == 'needs_id':
            observation_type = models.ObservationTypeChoices.INAT_NEEDS_ID
        elif quality_grade == 'casual':
            observation_type = models.ObservationTypeChoices.INAT_CASUAL
        else:
            observation_type = models.ObservationTypeChoices.UNKNOWN

        return models.ObservationType.objects.get(observation_type=observation_type)

    def get_coordinates(self):
        if self.metadata['geojson'] is None:
            return None, None

        coordinates = self.metadata['geojson']['coordinates']
        latitude, longitude = coordinates[0], coordinates[1]
        latitude = round(latitude, 12)
        longitude = round(longitude, 12)
        return latitude, longitude

    def get_verbatim_date(self):
        return self.metadata['observed_on']

    def get_date(self):
        return timezone.datetime.strptime(self.get_verbatim_date(), "%Y-%m-%d")

    def get_observer(self):
        return self.metadata['user']['login']

    def get_canonical_rank(self, name, rank):
        if rank == 'species':
            return models.TaxonRankChoices.SPECIES
        elif rank == 'hybrid':
            return models.TaxonRankChoices.HYBRID
        elif rank == 'variety':
            return models.TaxonRankChoices.VARIETY
        elif rank == 'subspecies':
            return models.TaxonRankChoices.SUBSPECIES

    def get_image_urls(self):
        for photo in self.metadata['photos']:
            if photo['url'] is not None:
                url = photo['url']
                if '/square.' in url:
                    small_url = url
                    medium_url = url.replace('/square.', '/medium.')
                    large_url = url.replace('/square.', '/large.')

                    yield small_url, models.ChecklistRecordImage.ImageSizeChoices.SMALL
                    yield medium_url, models.ChecklistRecordImage.ImageSizeChoices.MEDIUM
                    yield large_url, models.ChecklistRecordImage.ImageSizeChoices.LARGE


def read_full_checklist(checklist):
    if checklist.latest_date_retrieved is not None:
        start_date = checklist.latest_date_retrieved
    else:
        start_date = timezone.datetime(year=2015, month=1, day=1).date()
    end_date = timezone.now().date() - timezone.timedelta(days=2)
    years_to_update, months_to_update, dates_to_update = date_util.combine_date_ranges(
        list(date_util.date_range_list(start_date, end_date)))

    for year in years_to_update:
        print('\tUpdating for year {}'.format(year))
        InatChecklistReader(checklist, parameters={'year': year}).read_all()

    for year, month in months_to_update:
        print('\tUpdating for year {}, month {}'.format(year, month))
        InatChecklistReader(checklist, parameters={'year': year, 'month': month}).read_all()

    for date in dates_to_update:
        print('\tUpdating for date {}'.format(date))
        InatChecklistReader(checklist, parameters={'year': date.year, 'month': date.month,
                                                   'day': date.day}).read_all()

    checklist.latest_date_retrieved = end_date
    checklist.save()
