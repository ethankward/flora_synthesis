from django.db import transaction
from rest_framework import viewsets

from flora import models
from flora.models.taxon_synonym.api import serializers
from flora.util import api_crud


class TaxonSynonymViewSet(viewsets.ModelViewSet):
    queryset = models.TaxonSynonym.objects.all()
    serializer_class = serializers.TaxonSynonymSerializer


def create_taxon_synonym(request):
    taxon_id = request.data['taxon_id']
    synonym = request.data['synonym']

    taxon = models.Taxon.objects.get(pk=taxon_id)
    synonym = models.TaxonSynonym(
        taxon=taxon,
        synonym=synonym
    )
    with transaction.atomic():
        synonym.save()

    return synonym


def update_taxon_synonym(synonym_to_update, request):
    synonym_to_update.synonym = request.data['synonym']
    synonym_to_update.save()


crud_generator = api_crud.CRUDViewGenerator(
    model=models.TaxonSynonym,
    model_name="taxon_synonym",
    creation_function=create_taxon_synonym,
    update_function=update_taxon_synonym
)
