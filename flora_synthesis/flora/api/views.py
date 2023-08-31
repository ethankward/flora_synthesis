from django.db import transaction
from rest_framework import viewsets, views, status
from rest_framework.decorators import api_view
from rest_framework.exceptions import APIException
from rest_framework.response import Response

from flora import models
from flora.api import serializers
from flora.models.taxon.choices import taxon_endemic_statuses
from flora.models.taxon.choices import taxon_life_cycles


class ChecklistViewSet(viewsets.ModelViewSet):
    queryset = models.Checklist.objects.all()
    serializer_class = serializers.ChecklistSerializer


class ChecklistTaxonViewSet(viewsets.ModelViewSet):
    queryset = models.ChecklistTaxon.objects.all().select_related('family')
    serializer_class = serializers.ChecklistTaxonSerializer


class TaxonViewSet(viewsets.ModelViewSet):
    queryset = models.Taxon.objects.all().prefetch_related('subtaxa', 'taxonsynonym_set', 'taxon_checklist_taxa',
                                                           'taxon_checklist_taxa__checklist',
                                                           'taxon_checklist_taxa__all_mapped_taxa',
                                                           'taxon_checklist_taxa__family').select_related(
        'parent_species').order_by('family', 'taxon_name')
    serializer_class = serializers.TaxonSerializer

    def update(self, request, *args, **kwargs):
        obj = self.get_object()

        data_to_change = {'family': request.data.get("family", obj.family),
                          'life_cycle': request.data.get("life_cycle", obj.life_cycle),
                          'endemic': request.data.get("endemic", obj.endemic),
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


class TaxonAutocompleteViewSet(viewsets.ModelViewSet):
    queryset = models.Taxon.objects.all()
    serializer_class = serializers.TaxonNameSerializer

    def get_queryset(self):
        result = models.Taxon.objects.all().order_by('taxon_name')
        search_term = self.request.query_params.get('search_term', None)

        if search_term is not None:
            result = result.filter(taxon_name__icontains=search_term)

        return result


class TaxonSynonymViewSet(viewsets.ModelViewSet):
    queryset = models.TaxonSynonym.objects.all()
    serializer_class = serializers.TaxonSynonymSerializer


def get_checklist_record_data_item(record):
    data_item = {'id': record.id,
                 'external_id': record.external_id,
                 'last_refreshed': record.last_refreshed,
                 'checklist_taxon': record.checklist_taxon,
                 'mapped_taxon': record.mapped_taxon,
                 'checklist': record.checklist_taxon.checklist,
                 'date': None,
                 'observer': None}
    if hasattr(record, 'date'):
        data_item['date'] = record.date
    if hasattr(record, 'observer'):
        data_item['observer'] = record.observer

    return data_item


class ChecklistRecordView(views.APIView):
    def get(self, request, **kwargs):
        checklist_record_id = kwargs['checklist_record_id']
        checklist_type = kwargs['checklist_type']
        if checklist_type == 'f':
            record = models.FloraRecord.objects.get(pk=checklist_record_id)
        elif checklist_type == 's':
            record = models.SEINETRecord.objects.get(pk=checklist_record_id)
        elif checklist_type == 'i':
            record = models.InatRecord.objects.get(pk=checklist_record_id)
        else:
            raise APIException()

        return Response(serializers.ChecklistRecordSerializer(get_checklist_record_data_item(record)).data)


class ChecklistRecordsView(views.APIView):
    def get(self, request, **kwargs):
        print(kwargs)
        taxon_id = request.query_params.get('taxon_id', None)

        result = []
        for model in [models.FloraRecord, models.InatRecord, models.SEINETRecord]:
            for record in model.objects.filter(mapped_taxon=taxon_id).select_related('checklist_taxon',
                                                                                     'checklist_taxon__checklist',
                                                                                     'mapped_taxon'):
                result.append(get_checklist_record_data_item(record))

        return Response(serializers.ChecklistRecordSerializer(result, many=True).data)


class ChecklistTaxonFamilyViewSet(viewsets.ModelViewSet):
    queryset = models.ChecklistTaxonFamily.objects.all()
    serializer_class = serializers.ChecklistTaxonFamilySerializer


class LifeCycleView(views.APIView):
    def get(self, request):
        data = taxon_life_cycles.LifeCycleChoices.choices
        return Response(serializers.LifeCycleSerializer([{'value': i[0], 'text': i[1]} for i in data], many=True).data)


class EndemicView(views.APIView):
    def get(self, request):
        data = taxon_endemic_statuses.EndemicChoices.choices
        return Response(serializers.LifeCycleSerializer([{'value': i[0], 'text': i[1]} for i in data], many=True).data)


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
