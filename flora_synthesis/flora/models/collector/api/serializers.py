from rest_framework import serializers

from flora import models


class CollectorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Collector
        fields = [
            "id",
            "name",
            "external_url",
            "first_collection_year",
            "last_collection_year",
        ]


class CollectorSerializer(serializers.ModelSerializer):
    collector_aliases = serializers.SerializerMethodField()
    seinet_collection_records = serializers.SerializerMethodField()

    class Meta:
        model = models.Collector
        fields = [
            "id",
            "name",
            "external_url",
            "collector_aliases",
            "first_collection_year",
            "last_collection_year",
            "seinet_collection_records",
        ]

    def get_seinet_collection_records(self, obj):
        result = []
        for record in obj.collector_seinet_collection_records.all():
            if record.active:
                data_item = {
                    "id": record.id,
                    "external_id": record.external_id,
                    "date": record.date,
                    "external_url": record.external_url(),
                    "observation_type": record.get_observation_type_display(),
                    "taxon_name": record.checklist_taxon.taxon_name,
                    "observer": record.observer,
                }

                result.append(data_item)

        result.sort(key=lambda x: (x["date"] is None, x["date"]))
        return result

    def get_collector_aliases(self, obj):
        result = []
        for alias in obj.collector_aliases.all():
            result.append({"value": alias.id, "display": alias.alias})
        return result
