from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, List

from django.contrib.auth import get_user_model

from baserow.contrib.database.fields.models import Field
from baserow.core.registry import (
    CustomFieldsInstanceMixin,
    CustomFieldsRegistryMixin,
    Instance,
    ModelInstanceMixin,
    ModelRegistryMixin,
    Registry,
)

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
        :return: An unsaved Baserow field model object with the correct configuration.
        """


class DataSyncType(ModelInstanceMixin, CustomFieldsInstanceMixin, Instance, ABC):
    @abstractmethod
    def get_properties(self, instance) -> List[DataSyncProperty]:
        """
        Should return a list of property objects that define the schema of the synced
        table. It should list all the available properties, but the user can choose
        which ones they want to add. The `unique_primary` ones are required.

        :param instance: The model instance
        :param auth_data:
        :return: List of all properties in the data sync source.
        """

    @abstractmethod
    def get_all_rows(self, instance) -> List[Dict]:
        """
        Should return a list with dicts containing the raw row values. The values will
        run through the `to_baserow_value` method of the related property to convert
        them to the Baserow format. It must contain all the rows, even if there are
        many. It will be used to figure out:

        - Which rows don't exist, but in this list, and create those.
        - Which rows already exist, update those if changed.
        - Which rows exist, but not in this list, delete those.

        :param instance:
        :param auth_data:
        :return: List of all rows in the data sync source.
        """


class DataSyncTypeRegistry(ModelRegistryMixin, CustomFieldsRegistryMixin, Registry):
    name = "data_sync"


data_sync_type_registry = DataSyncTypeRegistry()
