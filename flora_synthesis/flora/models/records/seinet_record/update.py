import typing

from bs4 import BeautifulSoup
from django.utils import timezone

from flora.models.records.seinet_record.observation_types import SEINETObservationTypeChoices


def parse_seinet_date(date_str: str) -> typing.Optional[timezone.datetime]:
    if date_str in ['s.d.', 'unknown']:
        return

    date_formats = ["%Y-%m-%d"]

    for date_format in date_formats:
        try:
            return timezone.datetime.strptime(date_str, date_format)
        except ValueError:
            pass


class Updater:
    def __init__(self, data: dict):
        self.data = data
        self.soup = BeautifulSoup(data, 'html.parser')

    def get_div_value_if_present(self, div_id: str, func: typing.Callable[[str], typing.Any]) -> typing.Optional[str]:
        try:
            text = self.soup.find('div', attrs={'id': div_id}).text
        except AttributeError:
            return
        return func(text.replace('\t', '').replace('\xa0', ' ').strip())

    def get_title(self) -> str:
        return self.soup.find('div', attrs={'class': 'title1-div'}).text.strip()

    def is_general_research_observation(self) -> bool:
        return 'General Research Observations' in self.get_title()

    def is_collection(self) -> bool:
        return not self.is_general_research_observation()

    def get_observation_type(self) -> SEINETObservationTypeChoices:
        if self.is_general_research_observation():
            return SEINETObservationTypeChoices.GENERAL_RESEARCH
        else:
            return SEINETObservationTypeChoices.COLLECTION

    def get_herbarium_institution(self) -> typing.Optional[str]:
        if self.is_collection():
            return self.get_title()

    def get_verbatim_date(self) -> str:
        return self.get_div_value_if_present('verbeventid-div', lambda t: t.split(': ')[1])

    def get_date(self) -> str:
        return self.get_div_value_if_present('eventdate-div', lambda t: parse_seinet_date(t.split(': ')[1]))

    def get_verbatim_coordinates(self) -> str:
        return self.get_div_value_if_present('latlngdiv', lambda t: t)

    def get_coordinates(self) -> typing.Tuple[typing.Optional[float], typing.Optional[float]]:
        verbatim_coordinates = self.get_verbatim_coordinates()
        if verbatim_coordinates is not None:
            latitude = float(verbatim_coordinates.split(' ')[0])
            longitude = float(verbatim_coordinates.split(' ')[2])
            return latitude, longitude
        return None, None

    def get_verbatim_elevation(self) -> str:
        return self.get_div_value_if_present('elev-div', lambda t: t.split('\n')[-1])

    def get_observer(self) -> str:
        return self.get_div_value_if_present('recordedby-div', lambda t: t.split('\n')[1])

    def get_locality(self) -> str:
        return self.get_div_value_if_present('locality-div', lambda t: t.split('Locality: ')[1])
