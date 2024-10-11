from django.conf import settings
from django_q.tasks import async_task
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from flora import models
from flora.management.commands.import_inat_obs import import_inat_obs
from flora.models.checklist.api import serializers


class ChecklistViewSet(viewsets.ModelViewSet):
    queryset = models.Checklist.objects.all().order_by("checklist_name")
    serializer_class = serializers.ChecklistSerializer


class ChecklistStaleRecordCountViewSet(viewsets.ModelViewSet):
    queryset = models.Checklist.objects.all()
    serializer_class = serializers.ChecklistStaleRecordCount


class ChecklistStaleRecordViewSet(viewsets.ModelViewSet):
    queryset = models.Checklist.objects.all()
    serializer_class = serializers.ChecklistStaleRecordsSerializer


@api_view(["POST"])
def load_checklist(request):
    checklist_id = request.data["checklist_id"]
    checklist = models.Checklist.objects.get(pk=checklist_id)

    if settings.PRODUCTION:
        async_task(checklist.load)
    else:
        checklist.load()

    return Response(status=status.HTTP_200_OK)


@api_view(["POST"])
def retrieve_records(request):
    checklist_id = request.data["checklist_id"]
    n_records = request.data["n_records"]

    assert n_records <= 250
    checklist = models.Checklist.objects.get(pk=checklist_id)

    if settings.PRODUCTION:
        async_task(checklist.read_record_data, limit=n_records)
    else:
        checklist.read_record_data(limit=n_records)

    return Response(status=status.HTTP_200_OK)


@api_view(["POST"])
def retrieve_checklist_record(request):
    print('retrievign checklist record')
    record_id = request.data["record_id"]
    print(record_id)
    record = models.Record.objects.get(pk=record_id)
    print(record)
    checklist = models.Checklist.objects.get(pk=record.checklist.pk)
    print(checklist)

    if settings.PRODUCTION:
        async_task(checklist.read_specific_record_data, records=[record])
    else:
        checklist.read_specific_record_data(records=[record])


@api_view(["POST"])
def import_inat_observation(request):
    checklist_id = request.data["checklist_id"]
    observation_id = request.data["observation_id"]

    checklist = models.Checklist.objects.get(pk=checklist_id)

    import_inat_obs(checklist, observation_id)

    return Response(status=status.HTTP_200_OK)
