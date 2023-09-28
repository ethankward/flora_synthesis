from django.core.management import BaseCommand

from flora import models
from flora.models.taxon.choices import taxon_ranks


def check_chars(s: str):
    assert all([c in 'abcdefghijklmnopqrstuvwxyz-. ×' for c in s.lower()])


class TaxonRankFormatChecker:

    def __init__(self, name, rank, computed_genus):
        self.name = name
        self.rank = rank
        self.computed_genus = computed_genus
        self.parts = self.name.split(' ')

    def check_format(self):
        assert '  ' not in self.name
        assert '' not in self.parts
        assert [i == i.strip() for i in self.parts]
        check_chars(self.name)

        genus = self.parts[0]
        assert genus == self.computed_genus
        assert genus == genus.title()

        if self.rank == taxon_ranks.TaxonRankChoices.SPECIES:
            self.check_species()
        elif self.rank == taxon_ranks.TaxonRankChoices.SUBSPECIES:
            self.check_subspecies()
        elif self.rank == taxon_ranks.TaxonRankChoices.VARIETY:
            self.check_variety()
        elif self.rank == taxon_ranks.TaxonRankChoices.HYBRID:
            self.check_hybrid()
        elif self.rank == taxon_ranks.TaxonRankChoices.GENUS:
            self.check_genus()

    def check_species(self):
        assert len(self.parts) == 2
        assert self.parts[1] == self.parts[1].lower()

    def check_subspecies(self):
        assert len(self.parts) == 4

        assert self.parts[1] == self.parts[1].lower()
        assert self.parts[2] == 'subsp.'
        assert self.parts[3] == self.parts[3].lower()

    def check_variety(self):
        assert len(self.parts) == 4

        assert self.parts[1] == self.parts[1].lower()
        assert self.parts[2] == 'var.'
        assert self.parts[3] == self.parts[3].lower()

    def check_hybrid(self):
        assert len(self.parts) in [3, 4, 5]

        if len(self.parts) == 3:
            assert self.parts[1] == '×'
            assert self.parts[2] == self.parts[2].lower()
        elif len(self.parts) == 4:
            assert self.parts[1] == self.parts[1].lower()
            assert self.parts[2] == '×'
            assert self.parts[3] == self.parts[3].lower()
        elif len(self.parts) == 5:
            assert self.parts[1] == self.parts[1].lower()
            assert self.parts[2] == '×'
            assert self.parts[3] == self.parts[3].title()
            assert self.parts[4] == self.parts[4].lower()

    def check_genus(self):
        assert len(self.parts) == 2
        assert self.parts[1] == 'sp.'


def run():
    all_taxon_names = set([])

    for taxon in models.Taxon.objects.all():
        name = taxon.taxon_name
        rank = taxon.rank
        all_taxon_names.add(taxon.taxon_name)

        print([name, rank, taxon.pk])

        TaxonRankFormatChecker(name, rank, taxon.genus).check_format()

    for taxon_name in all_taxon_names:
        if 'var.' in taxon_name or 'subsp.' in taxon_name:
            if 'var.' in taxon_name:
                assert taxon_name.replace('var.', 'subsp.') not in all_taxon_names

            if 'subsp.' in taxon_name:
                assert taxon_name.replace('subsp.', 'var.') not in all_taxon_names

            parts = taxon_name.split(' ')
            if parts[1] != parts[3]:
                test_name = ' '.join([parts[0], parts[3]])
                print([taxon_name, test_name])
                assert test_name not in all_taxon_names


class Command(BaseCommand):

    def handle(self, *args, **options):
        run()
