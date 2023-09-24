from rest_framework import serializers

from flora import models


class CollectorAliasSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CollectorAlias
        fields = ['id', 'alias']
