from rest_framework import serializers

from flora import models


class ObservationDateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ObservationDate
        fields = ['date', 'url']
