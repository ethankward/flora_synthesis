from rest_framework import viewsets

from flora import models
from flora.models.personal_collection_record.api import serializers


class PersonalCollectionRecordViewSet(viewsets.ModelViewSet):
    queryset = models.PersonalCollectionRecord.objects.all().select_related('specific_taxon').order_by(
        '-collection_number')
    serializer_class = serializers.PersonalCollectionRecordSerializer
