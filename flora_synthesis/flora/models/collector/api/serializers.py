from rest_framework import serializers

from flora import models
from flora.models.collector_alias.api.serializers import CollectorAliasSerializer


class CollectorSerializer(serializers.ModelSerializer):
    collector_aliases = CollectorAliasSerializer(many=True, required=False)
    seinet_collection_records = serializers.SerializerMethodField()

    class Meta:
        model = models.Collector
        fields = ['id', 'name', 'external_url', 'collector_aliases', 'first_collection_year', 'last_collection_year',
                  'seinet_collection_records']

    def get_seinet_collection_records(self, obj):
        result = []
        for record in obj.collector_seinet_collection_records.all():
            if record.active:
                data_item = {'id': record.id,
                             'external_id': record.external_id,
                             'date': record.date,
                             'external_url': record.external_url(),
                             'observation_type': record.get_observation_type_display(),
                             'taxon_name': record.checklist_taxon.taxon_name
                             }

                result.append(data_item)

        return result
