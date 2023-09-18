from rest_framework import serializers

from flora import models


class PersonalCollectionRecordSerializer(serializers.ModelSerializer):
    specific_taxon_name = serializers.SerializerMethodField()
    status_display = serializers.SerializerMethodField()

    class Meta:
        model = models.PersonalCollectionRecord
        fields = ['id', 'date', 'status', 'status_display', 'inat_record_id', 'seinet_record_id', 'family',
                  'preliminary_taxon', 'specific_taxon', 'latitude', 'longitude', 'elevation_ft', 'locality',
                  'habitat',
                  'associated_collectors', 'associated_species', 'collection_number', 'time', 'specific_taxon_name',
                  'identification_notes', 'description', 'land_ownership']

    def get_status_display(self, obj):
        return obj.get_status_display()

    def get_specific_taxon_name(self, obj):
        if obj.specific_taxon:
            return obj.specific_taxon.taxon_name
