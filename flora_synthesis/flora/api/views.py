from rest_framework import viewsets, views
from rest_framework.exceptions import APIException
from rest_framework.response import Response

from flora import models
from flora.api import serializers


class TaxonViewSet(viewsets.ModelViewSet):
    queryset = models.Taxon.objects.all().prefetch_related('subtaxa', 'taxonsynonym_set',
                                                           'observation_types', 'on_checklists',
                                                           'taxon_checklist_taxa', 'taxon_checklist_taxa__family',
                                                           'taxon_checklist_taxa__observation_types').select_related(
        'parent_species').order_by('family', 'taxon_name')
    serializer_class = serializers.TaxonSerializer

    def update(self, request, *args, **kwargs):
        obj = self.get_object()

        data_to_change = {'family': request.data.get("family", obj.family),
                          'life_cycle': request.data.get("life_cycle", obj.life_cycle),
                          'endemic': request.data.get("endemic", obj.endemic),
                          'taxon_name': request.data.get("taxon_name", obj.taxon_name),
                          'seinet_id': request.data.get('seinet_id', obj.seinet_id),
                          'inat_id': request.data.get('inat_id', obj.seinet_id)
                          }

        serializer = self.serializer_class(data=data_to_change, partial=True, instance=self.get_object())

        if serializer.is_valid():
            self.perform_update(serializer)

            return Response(serializer.data)
        else:
            raise APIException()


class TaxonSynonymViewSet(viewsets.ModelViewSet):
    queryset = models.TaxonSynonym.objects.all()
    serializer_class = serializers.TaxonSynonymSerializer


class ChecklistViewSet(viewsets.ModelViewSet):
    queryset = models.Checklist.objects.all()
    serializer_class = serializers.ChecklistSerializer


class ChecklistRecordImagesViewSet(viewsets.ModelViewSet):
    queryset = models.ChecklistRecordImage.objects.all()
    serializer_class = serializers.ChecklistRecordImagesSerializer


class ChecklistRecordViewSet(viewsets.ModelViewSet):
    queryset = models.ChecklistRecord.objects.all()
    serializer_class = serializers.ChecklistRecordSerializer

    def get_queryset(self):
        result = models.ChecklistRecord.objects.all().select_related('checklist', 'checklist_taxon',
                                                                     'canonical_mapped_taxon',
                                                                     'observation_type').order_by('checklist', 'date')
        taxon_id = self.request.query_params.get('taxon_id', None)
        if taxon_id is not None and taxon_id.endswith('/'):
            taxon_id = taxon_id[:-1]
        if taxon_id is not None:
            result = result.filter(canonical_mapped_taxon=taxon_id)
        return result


class ObservationTypeViewSet(viewsets.ModelViewSet):
    queryset = models.ObservationType.objects.all()
    serializer_class = serializers.ObservationTypeSerializer


class ChecklistFamilyViewSet(viewsets.ModelViewSet):
    queryset = models.ChecklistFamily.objects.all()
    serializer_class = serializers.ChecklistFamilySerializer


class ChecklistTaxonViewSet(viewsets.ModelViewSet):
    queryset = models.ChecklistTaxon.objects.all().prefetch_related('mapped_taxa', 'observation_types').select_related(
        'family')
    serializer_class = serializers.ChecklistTaxonSerializer


class LifeCycleView(views.APIView):
    def get(self, request):
        data = models.Taxon.LifeCycleChoices.choices
        return Response(serializers.LifeCycleSerializer([{'value': i[0], 'text': i[1]} for i in data], many=True).data)


class EndemicView(views.APIView):
    def get(self, request):
        data = models.Taxon.EndemicChoices.choices
        return Response(serializers.LifeCycleSerializer([{'value': i[0], 'text': i[1]} for i in data], many=True).data)
