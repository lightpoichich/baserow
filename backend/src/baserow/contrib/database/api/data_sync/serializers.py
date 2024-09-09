from django.utils.functional import lazy

from rest_framework import serializers

from baserow.contrib.database.data_sync.models import DataSync, DataSyncProperty
from baserow.contrib.database.data_sync.registries import data_sync_type_registry


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
            "last_error",
        )


class CreateDataSyncSerializer(serializers.ModelSerializer):
    visible_properties = serializers.ListField(
        child=serializers.CharField(), required=True
    )
    type = serializers.ChoiceField(
        choices=lazy(data_sync_type_registry.get_types, list)(),
        help_text="The type of the data sync table that must be created.",
        required=True,
    )
    table_name = serializers.CharField(required=True)

    class Meta:
        model = DataSync
        fields = ("visible_properties", "type", "table_name")
