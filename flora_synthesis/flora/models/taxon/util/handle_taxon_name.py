from dataclasses import dataclass
from typing import Optional

from flora import models
from flora.models.taxon.choices import taxon_ranks


@dataclass
class TaxonName:
    original_name: str
    family: Optional[str] = None
    rank: Optional[taxon_ranks.TaxonRankChoices] = None
    genus: Optional[str] = None
    parent_species_name: Optional[str] = None
    canonical_name: Optional[str] = None

    def __init__(self, original_name: str, family: Optional[str] = None,
                 given_rank: Optional[taxon_ranks.TaxonRankChoices] = None):
        self.original_name = original_name
        self.family = family

        hybrid_xs = ['×', 'x']

        while '  ' in original_name:
            original_name = original_name.replace('  ', ' ')

        parts = original_name.split(' ')

        if len(parts) == 2:
            self.parse_species(parts)
        elif len(parts) == 3:
            if given_rank is not None:
                if given_rank == taxon_ranks.TaxonRankChoices.VARIETY:
                    self.parse_variety(parts)
                elif given_rank == taxon_ranks.TaxonRankChoices.SUBSPECIES:
                    self.parse_subspecies(parts)

            if parts[1] in hybrid_xs:
                self.parse_hybrid(parts)

        elif len(parts) == 4:
            if parts[2] == 'var.':
                self.parse_variety(parts, var_index=3)

            elif parts[2] == 'subsp.':
                self.parse_subspecies(parts, ssp_index=3)

            elif parts[2] in hybrid_xs:
                self.parse_hybrid(parts, h_index=3)
        elif len(parts) == 5:
            if parts[2] in hybrid_xs:
                self.parse_species_hybrid(parts)
        elif len(parts) == 6:
            if parts[2] == 'subsp.' and parts[4] == 'var.':
                self.parse_subspecies_variety(parts)
        else:
            raise ValueError("Could not parse name: {}, {}".format(original_name, self.rank))

    def parse_species(self, parts):
        self.rank = taxon_ranks.TaxonRankChoices.SPECIES

        genus = parts[0].title()
        specific_epithet = parts[1].lower()

        self.genus = genus
        self.canonical_name = '{} {}'.format(genus, specific_epithet)

    def parse_variety(self, parts, var_index=2):
        self.rank = taxon_ranks.TaxonRankChoices.VARIETY

        genus = parts[0].title()
        specific_epithet = parts[1].lower()
        variety = parts[var_index].lower()

        self.genus = genus
        self.parent_species_name = '{} {}'.format(genus, specific_epithet)
        self.canonical_name = '{} {} var. {}'.format(genus, specific_epithet, variety)

    def parse_subspecies(self, parts, ssp_index=2):
        self.rank = taxon_ranks.TaxonRankChoices.SUBSPECIES

        genus = parts[0].title()
        specific_epithet = parts[1].lower()
        subspecies = parts[ssp_index].lower()

        self.genus = genus
        self.parent_species_name = '{} {}'.format(genus, specific_epithet)
        self.canonical_name = '{} {} subsp. {}'.format(genus, specific_epithet, subspecies)

    def parse_subspecies_variety(self, parts):
        self.rank = taxon_ranks.TaxonRankChoices.SUBSPECIES_VARIETY
        genus = parts[0].title()
        specific_epithet = parts[1].lower()
        subspecies = parts[3].lower()
        variety = parts[5].lower()

        self.genus = genus
        self.parent_species_name = '{} {}'.format(genus, specific_epithet)
        self.canonical_name = '{} {} subsp. {} var. {}'.format(genus, specific_epithet, subspecies, variety)

    def parse_hybrid(self, parts, h_index=2):
        self.rank = taxon_ranks.TaxonRankChoices.HYBRID

        genus = parts[0].title()
        name = parts[h_index]

        self.genus = genus
        self.canonical_name = '{} × {}'.format(genus, name)

    def parse_species_hybrid(self, parts):
        self.rank = taxon_ranks.TaxonRankChoices.HYBRID

        genus = parts[0].title()
        self.genus = genus
        self.canonical_name = '{} {} × {} {}'.format(genus, parts[1], parts[3], parts[4])

    def get_db_item(self):
        try:
            synonym = models.TaxonSynonym.objects.get(synonym=self.canonical_name)
            return synonym.taxon
        except models.TaxonSynonym.DoesNotExist:
            pass

        try:
            existing = models.Taxon.objects.get(taxon_name=self.canonical_name)
            return existing
        except models.Taxon.DoesNotExist:
            pass

        if self.family is None:
            self.family = input("Enter family for taxon {}: ".format(self.original_name))

        if self.parent_species_name is not None:
            parent_species = TaxonName(self.parent_species_name, family=self.family).get_db_item()
        else:
            parent_species = None

        db_taxon, created = models.Taxon.objects.get_or_create(
            genus=self.genus,
            family=self.family,
            parent_species=parent_species,
            taxon_name=self.canonical_name,
            rank=self.rank
        )
        if created:
            print('Created new taxon: {}'.format(db_taxon))

        if parent_species is not None:
            parent_species.subtaxa.add(db_taxon)

        return db_taxon
