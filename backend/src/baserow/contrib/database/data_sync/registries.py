from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Callable, Dict, List

from django.contrib.auth import get_user_model

from baserow.contrib.database.data_sync.export_serialized import (
    DataSyncExportSerializedStructure,
)
from baserow.contrib.database.fields.models import Field
from baserow.core.registry import (
    CustomFieldsInstanceMixin,
    CustomFieldsRegistryMixin,
    ImportExportMixin,
    Instance,
    ModelInstanceMixin,
    ModelRegistryMixin,
    Registry,
)

if TYPE_CHECKING:
    from baserow.contrib.database.data_sync.models import DataSync

User = get_user_model()

ExporterFunc = Callable[[Any, bool], None]


class DataSyncProperty(ABC):
    unique_primary = False
    """
    Indicates whether this property is used to identify a unique row. This will be used
    to identify if a row must be created, updated, or deleted. There must at least be
    one. If multiple are provided, then a unique combination will be used. It's not
    possible for the user to exclude them in the table.
    """

    def __init__(self, key, name):
        """
        :param key: A unique key that must never be changed.
        :param name: Human-readable name of the property.
        """

        self.key = key
        self.name = name

    @abstractmethod
    def to_baserow_field(self) -> Field:
        """
        Should return an unsaved Baserow field instance. This is the field object that
        will be used to automatically create the field.

        :return: An unsaved Baserow field model object.
        """

    def is_equal(self, baserow_row_value: Any, data_sync_row_value: Any) -> bool:
        """
        Checks if the provided cell value is equal. This is used to check if the
        row must be updated.

        :param baserow_row_value: The row value from the Baserow row.
        :param data_sync_row_value:  The row value from the data sync `get_all_rows`
            row.
        :return: `True` if the value is equal.
        """

        return baserow_row_value == data_sync_row_value


class DataSyncType(
    ModelInstanceMixin, CustomFieldsInstanceMixin, ImportExportMixin, Instance, ABC
):
    @abstractmethod
    def get_properties(self, instance: "DataSync") -> List[DataSyncProperty]:
        """
        Should return a list of property objects that define the schema of the synced
        table. It should list all the available properties, but the user can choose
        which ones they want to add. The `unique_primary` ones are required.

        A property can be changed to another type, but the field will only be updated
        for the user if they make any change in the visible fields. It's therefore
        recommended to keep either the `get_all_rows` value of the field compatible
        with both the new and old field type, or introduce a new property with a
        different key.

        It's okay to delete or add properties. If they're deleted, then they the
        field will persistent until the user changes the visible fields, but when
        syncing the cell value remains empty. A new property can be added by the
        user by changing the visible fields.

        :param instance: The data sync instance of which the properties must be
            returned.
        :return: List of all properties in the data sync source.
        """

    @abstractmethod
    def get_all_rows(self, instance: "DataSync") -> List[Dict]:
        """
        Should return a list with dicts containing the raw row values. The values will
        run through the `to_baserow_value` method of the related property to convert
        them to the Baserow format. It must contain all the rows, even if there are
        many. It will be used to figure out:

        - Which rows don't exist, but in this list, and create those.
        - Which rows already exist, update those if changed.
        - Which rows exist, but not in this list, delete those.

        :param instance: The data sync instance of which the rows must be fetched.
        :raises SyncError: If something goes wrong, but don't want to fail hard and
            expose the error via the API.
        :return: List of all rows in the data sync source.
        """

    def export_serialized(self, instance: "DataSync"):
        """
        Exports the data sync properties and the `allowed_fields` to the serialized
        format.
        """

        properties = instance.data_sync_properties.all()
        type_specific = {
            field: getattr(instance, field) for field in self.allowed_fields
        }
        return DataSyncExportSerializedStructure.data_sync(
            id=instance.id,
            type_name=self.type,
            last_sync=instance.last_sync.isoformat(),
            last_error=instance.last_error,
            properties=[
                DataSyncExportSerializedStructure.property(
                    key=p.key, field_id=p.field_id
                )
                for p in properties
            ],
            **type_specific,
        )

    def import_serialized(self, table, serialized_values, id_mapping):
        """
        Imports the data sync properties and the `allowed_fields`.
        """

        from .models import DataSyncProperty as DataSyncPropertyModel

        if "database_table_data_sync" not in id_mapping:
            id_mapping["database_table_data_sync"] = {}

        serialized_copy = serialized_values.copy()
        original_id = serialized_copy.pop("id")
        properties = serialized_copy.pop("properties", [])
        serialized_copy.pop("type")
        type_properties = {
            field: serialized_copy.get(field) for field in self.allowed_fields
        }
        data_sync = self.model_class.objects.create(
            table=table,
            last_sync=serialized_copy["last_sync"],
            last_error=serialized_copy["last_error"],
            **type_properties,
        )

        properties_to_be_created = []
        for property in properties:
            properties_to_be_created.append(
                DataSyncPropertyModel(
                    data_sync=data_sync,
                    field_id=id_mapping["database_fields"][property["field_id"]],
                    key=property["key"],
                )
            )

        DataSyncPropertyModel.objects.bulk_create(properties_to_be_created)

        id_mapping["database_table_data_sync"][original_id] = data_sync.id

        return data_sync


class DataSyncTypeRegistry(ModelRegistryMixin, CustomFieldsRegistryMixin, Registry):
    name = "data_sync"


data_sync_type_registry = DataSyncTypeRegistry()
