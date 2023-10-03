from django.core.management import BaseCommand

from flora import models
from flora.models.taxon.choices.taxon_ranks import TaxonRankChoices


def run():
    for taxon in (
        models.Taxon.objects.all()
        .select_related("parent_species")
        .prefetch_related(
            "subtaxa", "parent_species__subtaxa", "subtaxa__parent_species"
        )
        .order_by("taxon_name")
    ):

        print([taxon, taxon.pk])

        parent = taxon.parent_species
        subtaxa = list(taxon.subtaxa.all())

        has_parent = parent is not None
        has_subtaxa = len(subtaxa) > 0

        assert not (has_parent and has_subtaxa)

        assert taxon not in subtaxa
        assert taxon != parent

        if taxon.rank in [TaxonRankChoices.SUBSPECIES, TaxonRankChoices.VARIETY]:
            assert has_parent

        if has_parent:
            assert taxon in parent.subtaxa.all()
            assert taxon.rank in [TaxonRankChoices.SUBSPECIES, TaxonRankChoices.VARIETY]

            assert taxon.genus == parent.genus
            assert taxon.family == parent.family

        if has_subtaxa:
            assert taxon.rank == TaxonRankChoices.SPECIES

            for subtaxon in subtaxa:
                assert subtaxon.parent_species == taxon
                assert subtaxon.rank in [
                    TaxonRankChoices.SUBSPECIES,
                    TaxonRankChoices.VARIETY,
                ]
                assert taxon.genus == subtaxon.genus
                assert taxon.family == subtaxon.family


class Command(BaseCommand):
    def handle(self, *args, **options):
        run()
