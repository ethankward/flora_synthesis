from django.conf import settings
from django_q.tasks import async_task
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from flora import models
from flora.models.checklist.api import serializers


class ChecklistViewSet(viewsets.ModelViewSet):
    queryset = models.Checklist.objects.all()
    serializer_class = serializers.ChecklistSerializer


class ChecklistStaleRecordCountViewSet(viewsets.ModelViewSet):
    queryset = models.Checklist.objects.all()
    serializer_class = serializers.ChecklistStaleRecordCount


@api_view(['POST'])
def update(request):
    checklist_id = request.data['checklist_id']
    page = request.data['page']
    checklist = models.Checklist.objects.get(pk=checklist_id)

    if settings.PRODUCTION:
        async_task(checklist.load, kwargs={'page': page})
    else:
        checklist.load(page=page)

    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
def retrieve(request):
    checklist_id = request.data['checklist_id']
    n_records = request.data['n_records']

    assert n_records in [10, 25, 50]
    checklist = models.Checklist.objects.get(pk=checklist_id)

    async_task(checklist.read_record_data, kwargs={'limit': n_records})

    return Response(status=status.HTTP_200_OK)
