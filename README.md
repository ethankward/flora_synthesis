![flake8](https://github.com/ethankward/flora_synthesis/actions/workflows/main.yml/badge.svg)
![Tests](https://github.com/ethankward/flora_synthesis/actions/workflows/test_django.yml/badge.svg)

Django backend to synthesize floristic data from several sources:
* SEINet (https://swbiodiversity.org)
* iNaturalist (https://www.inaturalist.org)
* Locally generated checklists

Manages synonyms, taxonomic names and other identifiers, collection dates, and provides an API.

## Importing checklists
Use the `manage.py add_new_checklist` command to create a new checklist from one of these sources.

### Local checklists from files ###
Local flora data can be provided as a list in JSON format with the following fields:
* `checklist_taxon_name`: the taxon name as it appears in the checklist
* `checklist_taxon_family`: the taxon family as it appears in the checklist
* `external_id` (optional): an external ID for the record
* `observation_type` (optional): One of `present`, `missing`, `suspected`, or `unknown`.
* `mapped_taxon_name` (optional): A canonical taxon for the checklist record
* `note` (optional): any note for the taxon
