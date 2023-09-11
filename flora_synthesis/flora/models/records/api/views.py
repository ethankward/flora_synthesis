from django.db import transaction
from rest_framework import views, status
from rest_framework.decorators import api_view
from rest_framework.exceptions import APIException
from rest_framework.response import Response

from flora import models
from flora.models.records.api import serializers


def get_checklist_record_data_item(record):
    data_item = {'id': record.id,
                 'external_id': record.external_id,
                 'last_refreshed': record.last_refreshed,
                 'checklist_taxon': record.checklist_taxon,
                 'mapped_taxon': record.mapped_taxon,
                 'checklist': record.checklist_taxon.checklist,
                 'date': None,
                 'observer': None,
                 'external_url': record.external_url(),
                 'observation_type': record.get_observation_type_display(),
                 'notes': list(record.notes.all())}

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
        taxon_id = request.query_params.get('taxon_id', None)

        result = []
        if taxon_id is not None:
            taxon = models.Taxon.objects.get(pk=taxon_id)

            for model in [models.FloraRecord, models.InatRecord, models.SEINETRecord]:
                for record in model.objects.filter(mapped_taxon=taxon).select_related('checklist_taxon',
                                                                                      'checklist_taxon__checklist',
                                                                                      'mapped_taxon'):
                    result.append(get_checklist_record_data_item(record))
                for subtaxon in taxon.subtaxa.all():
                    for record in model.objects.filter(mapped_taxon=subtaxon).select_related('checklist_taxon',
                                                                                             'checklist_taxon__checklist',
                                                                                             'mapped_taxon'):
                        result.append(get_checklist_record_data_item(record))

        return Response(serializers.ChecklistRecordSerializer(result, many=True).data)


@api_view(['POST'])
def update_checklist_record_mapped_taxon(request):
    if request.method != 'POST':
        return

    checklist_type = request.data['checklist_type']
    checklist_record_id = request.data['checklist_record_id']
    mapped_to_id = request.data['mapped_to_id']

    mapped_taxon = models.Taxon.objects.get(pk=mapped_to_id)

    if checklist_type == 'f':
        checklist_record = models.FloraRecord.objects.get(pk=checklist_record_id)
    elif checklist_type == 's':
        checklist_record = models.SEINETRecord.objects.get(pk=checklist_record_id)
    elif checklist_type == 'i':
        checklist_record = models.InatRecord.objects.get(pk=checklist_record_id)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    with transaction.atomic():
        checklist_record.mapped_taxon = mapped_taxon
        checklist_record.save()
        checklist_record.checklist_taxon.save()

    return Response(status=status.HTTP_200_OK)
