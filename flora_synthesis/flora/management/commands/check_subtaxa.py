"""
Check that subtaxa are properly represented in the database.
"""
from django.core.management import BaseCommand

from flora import models
from flora.models.taxon.choices.taxon_ranks import TaxonRankChoices


def run():
    all_subtaxa_ranks = [TaxonRankChoices.SUBSPECIES, TaxonRankChoices.VARIETY]

    for taxon in (
            models.Taxon.objects.all()
                    .select_related("parent_species")
                    .prefetch_related(
                "subtaxa", "parent_species__subtaxa", "subtaxa__parent_species"
            )
                    .order_by("taxon_name")
    ):

        parent = taxon.parent_species
        subtaxa = list(taxon.subtaxa.all())

        has_parent = parent is not None
        has_subtaxa = len(subtaxa) > 0

        # only a single level (no subtaxa with subtaxa, or parents with parents)
        assert not (has_parent and has_subtaxa)

        # taxon is not its own subtaxon or parent
        assert taxon not in subtaxa
        assert taxon != parent

        # subspecies and varieties have parents
        if taxon.rank in all_subtaxa_ranks:
            assert has_parent

        if has_parent:
            # subtaxon is in parent subtaxa
            assert taxon in parent.subtaxa.all()

            # taxon with parent is a subtaxon
            assert taxon.rank in all_subtaxa_ranks

            # same genus and family as parent
            assert taxon.genus == parent.genus
            assert taxon.family == parent.family

        if has_subtaxa:
            # parent is a species
            assert taxon.rank == TaxonRankChoices.SPECIES

            for subtaxon in subtaxa:
                # parent is parent of subtaxon
                assert subtaxon.parent_species == taxon

                # subtaxon rank
                assert subtaxon.rank in all_subtaxa_ranks

                # same genus and family as subtaxon
                assert taxon.genus == subtaxon.genus
                assert taxon.family == subtaxon.family


class Command(BaseCommand):
    def handle(self, *args, **options):
        run()
