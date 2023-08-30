import itertools
import json
import typing

from requests_ratelimiter import LimiterSession


class InatApi:
    def __init__(self, session: LimiterSession):
        self.session = session

    def read_api_data(self, url: str, parameters: dict, paginate: bool = True) -> typing.Generator[dict, None, None]:
        if not paginate:
            data = json.loads(self.session.get(url, params={**parameters}).text)
            results = data['results']
            yield from results
        else:
            for page in itertools.count(1):
                data = json.loads(self.session.get(url, params={**parameters, **{'page': page}}).text)
                results = data['results']
                if len(results) == 0:
                    break
                yield from results

    def get_urls_with_ids(self, base_url: str, ids: typing.List[int] = None):
        if ids is None:
            yield base_url
        else:
            size = 30
            for i in range(len(ids)//size + 1):
                taxon_ids_comma_delimited = ','.join(map(str, ids[size*i:size*(i + 1)]))
                url = base_url + '/' + taxon_ids_comma_delimited
                yield url

    def read_observation_data(self, parameters: dict, observation_ids: typing.List[int] = None):
        base_url = "https://api.inaturalist.org/v1/observations"
        for url in self.get_urls_with_ids(base_url, observation_ids):
            yield from self.read_api_data(url, parameters, paginate=False)

    def read_taxon_data(self, taxon_ids: typing.List[int]):
        base_url = "https://api.inaturalist.org/v1/taxa"
        for url in self.get_urls_with_ids(base_url, taxon_ids):
            yield from self.read_api_data(url, {}, paginate=False)
