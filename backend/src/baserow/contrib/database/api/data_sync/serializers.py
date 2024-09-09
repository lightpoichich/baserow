from rest_framework import serializers

from baserow.contrib.database.data_sync.models import DataSync, DataSyncProperty


class DataSyncPropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = DataSyncProperty
        fields = (
            "field_id",
            "key",
        )


class DataSyncSerializer(serializers.ModelSerializer):
    data_sync_properties = DataSyncPropertySerializer(many=True)

    class Meta:
        model = DataSync
        fields = (
            "id",
            "data_sync_properties",
            "last_sync",
        )
