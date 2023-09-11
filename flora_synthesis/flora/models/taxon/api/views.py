from django.db import transaction
from rest_framework import viewsets, views, status
from rest_framework.decorators import api_view
from rest_framework.exceptions import APIException
from rest_framework.response import Response

from flora import models
from flora.models.taxon.api import serializers
from flora.models.taxon.choices import taxon_endemic_statuses, taxon_life_cycles, taxon_introduced_statuses


class TaxonViewSet(viewsets.ModelViewSet):
    queryset = models.Taxon.objects.all()
    serializer_class = serializers.TaxonSerializer

    def get_queryset(self):
        result = models.Taxon.objects.all().prefetch_related('subtaxa', 'taxonsynonym_set', 'taxon_checklist_taxa',
                                                             'taxon_checklist_taxa__checklist',
                                                             'taxon_checklist_taxa__all_mapped_taxa',
                                                             'taxon_checklist_taxa__family').select_related(
            'parent_species', 'first_observation_date', 'last_observation_date')

        checklist_id = self.request.query_params.get('checklist', None)
        genus = self.request.query_params.get('genus', None)
        family = self.request.query_params.get('family', None)

        if checklist_id is not None:
            result = result.filter(taxon_checklist_taxa__checklist=checklist_id)

        if genus is not None:
            result = result.filter(genus=genus)

        if family is not None:
            result = result.filter(family=family)

        result = result.order_by('family', 'taxon_name')

        return result

    def update(self, request, *args, **kwargs):
        obj = self.get_object()

        data_to_change = {'family': request.data.get("family", obj.family),
                          'life_cycle': request.data.get("life_cycle", obj.life_cycle),
                          'endemic': request.data.get("endemic", obj.endemic),
                          'introduced': request.data.get("introduced", obj.introduced),
                          'taxon_name': request.data.get("taxon_name", obj.taxon_name),
                          'seinet_id': request.data.get('seinet_id', obj.seinet_id),
                          'inat_id': request.data.get('inat_id', obj.inat_id)
                          }

        serializer = self.serializer_class(data=data_to_change, partial=True, instance=self.get_object())

        if serializer.is_valid():
            self.perform_update(serializer)

            return Response(serializer.data)
        else:
            raise APIException()


class PrimaryChecklistTaxonViewSet(viewsets.ModelViewSet):
    queryset = models.Taxon.objects.all()
    serializer_class = serializers.MinimalTaxonSerializer

    def get_queryset(self):
        result = models.Taxon.objects.all().select_related('first_observation_date', 'last_observation_date').order_by(
            'taxon_name')
        result = result.filter(taxon_checklist_taxa__checklist__primary_checklist=True).distinct()
        return result


class TaxonAutocompleteViewSet(viewsets.ModelViewSet):
    queryset = models.Taxon.objects.all()
    serializer_class = serializers.TaxonNameSerializer

    def get_queryset(self):
        result = models.Taxon.objects.all().order_by('taxon_name')
        search_term = self.request.query_params.get('search_term', None)

        if search_term is not None:
            result = result.filter(taxon_name__icontains=search_term)

        return result


class FamiliesListView(views.APIView):
    def get(self, request):
        data = models.Taxon.objects.all().filter(taxon_checklist_taxa__checklist__primary_checklist=True).order_by(
            'family').values_list('family').distinct()
        return Response(serializers.TaxonFamilySerializer([{'family': family[0]} for family in data], many=True).data)


class LifeCycleView(views.APIView):
    def get(self, request):
        data = taxon_life_cycles.LifeCycleChoices.choices
        return Response(
            serializers.LifeCycleSerializer([{'value': i[0], 'display': i[1]} for i in data], many=True).data)


class EndemicView(views.APIView):
    def get(self, request):
        data = taxon_endemic_statuses.EndemicChoices.choices
        return Response(serializers.EndemicSerializer([{'value': i[0], 'display': i[1]} for i in data], many=True).data)


class IntroducedView(views.APIView):
    def get(self, request):
        data = taxon_introduced_statuses.IntroducedChoices.choices
        return Response(
            serializers.IntroducedSerializer([{'value': i[0], 'display': i[1]} for i in data], many=True).data)


@api_view(['POST'])
def make_synonym_of(request):
    if request.method != 'POST':
        return

    taxon_id_1 = request.data['taxon_id_1']
    taxon_id_2 = request.data['taxon_id_2']

    taxon_1 = models.Taxon.objects.get(pk=taxon_id_1)
    taxon_2 = models.Taxon.objects.get(pk=taxon_id_2)

    synonym = models.TaxonSynonym(
        synonym=taxon_1.taxon_name,
        taxon=taxon_2
    )
    with transaction.atomic():
        synonym.save()

    return Response(status=status.HTTP_200_OK)
