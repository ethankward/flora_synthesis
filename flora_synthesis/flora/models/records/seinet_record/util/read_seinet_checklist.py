import typing

from bs4 import BeautifulSoup

from flora import models
from flora.models.records.util import checklist_reader
from flora.models.taxon.choices import taxon_ranks
from flora.models.taxon.util import handle_taxon_name
from flora.util import http_util

SESSION = http_util.get_session()


def get_canonical_rank(name: str) -> typing.Optional[taxon_ranks.TaxonRankChoices]:
    try:
        return handle_taxon_name.TaxonName(name).rank
    except ValueError:
        return


class SEINETChecklistReader(checklist_reader.ChecklistReader):
    checklist_record_type = models.SEINETRecord

    def __init__(self, checklist):
        super().__init__(checklist)
        self.seinet_checklist_id = checklist.external_checklist_id
        self.base_url = "https://swbiodiversity.org/seinet/checklists/checklist.php?clid=%s"%self.seinet_checklist_id

    def get_soup(self, page):
        return BeautifulSoup(SESSION.get(self.base_url, params={'pagenumber': page}).text, 'html.parser')

    def total_pages(self):
        soup = self.get_soup(1)

        for div in soup.find_all('div', {'class': 'printoff'}):
            if 'Page 1 of ' in div.text:
                return int(div.text.split('1 of ')[1].split(':')[0])

    def generate_data(self) -> typing.Generator[checklist_reader.ChecklistReadItem, None, None]:
        total_pages = self.total_pages()
        if total_pages is None:
            return
        family_name = None
        family = None

        for page in range(1, total_pages + 1):
            soup = self.get_soup(page)

            taxalist_div = soup.find('div', attrs={'id': 'taxalist-div'})

            for div in taxalist_div.find_all('div'):
                classes = div.get('class', [])
                if 'family-div' in classes:
                    family_name = div.text.strip().title()
                    family, _ = models.ChecklistTaxonFamily.objects.get_or_create(
                        checklist=self.checklist, family=family_name
                    )

                if 'taxon-container' in classes:
                    taxon_name = div.find('span', attrs={'class': 'taxon-span'}).text
                    notes_div = div.find('div', attrs={'class': 'note-div'})
                    taxon_id = int(div.get('id').split('-')[1])
                    count = 0
                    canonical_rank = get_canonical_rank(
                        taxon_name)
                    if canonical_rank is not None:
                        if notes_div is not None:
                            for record_a in notes_div.find_all('a'):
                                record_id = int(record_a.get('onclick').split('(')[1].split(')')[0])
                                record_css_id = record_a.get('id', '')

                                if not record_css_id.startswith('lessvouch') and not record_css_id.startswith(
                                        'morevouch'):
                                    yield checklist_reader.ChecklistReadItem(
                                        checklist_family=family,
                                        taxon_name=taxon_name,
                                        taxon_id=str(taxon_id),
                                        record_id=str(record_id),
                                        observation_data=None,
                                        given_rank=canonical_rank.name.lower(),
                                        canonical_rank=canonical_rank
                                    )
                                    count += 1
                        if count == 0:
                            yield checklist_reader.ChecklistReadItem(checklist_family=family,
                                                                     taxon_name=taxon_name,
                                                                     taxon_id=str(taxon_id),
                                                                     record_id="placeholder_{}_{}".format(taxon_name,
                                                                                                          taxon_id),
                                                                     observation_data=None,
                                                                     given_rank=canonical_rank.name.lower(),
                                                                     is_placeholder=True,
                                                                     canonical_rank=canonical_rank)
