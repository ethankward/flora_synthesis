from rest_framework import viewsets

from flora import models
from flora.api import serializers


class ChecklistViewSet(viewsets.ModelViewSet):
    queryset = models.Checklist.objects.all()
    serializer_class = serializers.ChecklistSerializer


class ChecklistTaxonViewSet(viewsets.ModelViewSet):
    queryset = models.ChecklistTaxon.objects.all().select_related('family')
    serializer_class = serializers.ChecklistTaxonSerializer


#
# class TaxonViewSet(viewsets.ModelViewSet):
#     queryset = models.Taxon.objects.all().prefetch_related('subtaxa', 'taxonsynonym_set',
#                                                            'taxon_checklist_taxa', 'taxon_checklist_taxa__family',
#                                                            'taxon_checklist_taxa__observation_types').select_related(
#         'parent_species').order_by('family', 'taxon_name')
#     serializer_class = serializers.TaxonSerializer
#
#     def update(self, request, *args, **kwargs):
#         obj = self.get_object()
#
#         data_to_change = {'family': request.data.get("family", obj.family),
#                           'life_cycle': request.data.get("life_cycle", obj.life_cycle),
#                           'endemic': request.data.get("endemic", obj.endemic),
#                           'taxon_name': request.data.get("taxon_name", obj.taxon_name),
#                           'seinet_id': request.data.get('seinet_id', obj.seinet_id),
#                           'inat_id': request.data.get('inat_id', obj.inat_id)
#                           }
#
#         serializer = self.serializer_class(data=data_to_change, partial=True, instance=self.get_object())
#
#         if serializer.is_valid():
#             self.perform_update(serializer)
#
#             return Response(serializer.data)
#         else:
#             raise APIException()
#
#
# class TaxonAutocompleteViewSet(viewsets.ModelViewSet):
#     queryset = models.Taxon.objects.all()
#     serializer_class = serializers.TaxonNameSerializer
#
#     def get_queryset(self):
#         result = models.Taxon.objects.all().order_by('taxon_name')
#         search_term = self.request.query_params.get('search_term', None)
#
#         if search_term is not None:
#             result = result.filter(taxon_name__icontains=search_term)
#
#         return result
#
#
# class TaxonSynonymViewSet(viewsets.ModelViewSet):
#     queryset = models.TaxonSynonym.objects.all()
#     serializer_class = serializers.TaxonSynonymSerializer
#
#

# class ChecklistRecordImagesViewSet(viewsets.ModelViewSet):
#     queryset = models.ChecklistRecordImage.objects.all()
#     serializer_class = serializers.ChecklistRecordImagesSerializer
#
#
# class ChecklistRecordViewSet(viewsets.ModelViewSet):
#     queryset = models.ChecklistRecord.objects.all()
#     serializer_class = serializers.ChecklistRecordSerializer
#
#     def get_queryset(self):
#         result = models.ChecklistRecord.objects.all().select_related('checklist', 'checklist_taxon',
#                                                                      'canonical_mapped_taxon',
#                                                                      'observation_type').filter(active=True).order_by(
#             'checklist', 'date')
#         taxon_id = self.request.query_params.get('taxon_id', None)
#         if taxon_id is not None and taxon_id.endswith('/'):
#             taxon_id = taxon_id[:-1]
#         if taxon_id is not None:
#             result = result.filter(canonical_mapped_taxon=taxon_id)
#         return result
#
#
# class ObservationTypeViewSet(viewsets.ModelViewSet):
#     queryset = models.ObservationType.objects.all()
#     serializer_class = serializers.ObservationTypeSerializer
#
#
# class ChecklistFamilyViewSet(viewsets.ModelViewSet):
#     queryset = models.ChecklistFamily.objects.all()
#     serializer_class = serializers.ChecklistFamilySerializer
#
#

#
# class LifeCycleView(views.APIView):
#     def get(self, request):
#         data = models.Taxon.LifeCycleChoices.choices
#         return Response(serializers.LifeCycleSerializer([{'value': i[0], 'text': i[1]} for i in data], many=True).data)
#
#
# class EndemicView(views.APIView):
#     def get(self, request):
#         data = models.Taxon.EndemicChoices.choices
#         return Response(serializers.LifeCycleSerializer([{'value': i[0], 'text': i[1]} for i in data], many=True).data)
#
#
# @api_view(['POST'])
# def make_synonym_of(request):
#     if request.method != 'POST':
#         return
#
#     taxon_id_1 = request.data['taxon_id_1']
#     taxon_id_2 = request.data['taxon_id_2']
#
#     taxon_1 = models.Taxon.objects.get(pk=taxon_id_1)
#     taxon_2 = models.Taxon.objects.get(pk=taxon_id_2)
#
#     synonym = models.TaxonSynonym(
#         synonym=taxon_1.taxon_name,
#         taxon=taxon_2
#     )
#     with transaction.atomic():
#         synonym.save()
#
#     return Response(status=status.HTTP_200_OK)
