from abc import ABC, abstractmethod
from typing import Any

from baserow.core.models import Group
from baserow.core.registries import application_type_registry
from baserow.core.registry import (
    ModelRegistryMixin,
    Registry,
    ModelInstanceMixin,
    Instance,
)
from baserow.core.signals import group_created


class TrashableItemTypeRegistry(ModelRegistryMixin, Registry):
    """
    The TrashableItemTypeRegistry contains models which can be "trashed" in baserow.
    When an instance of a trashable model is trashed it is removed from baserow but
    not permanently. Once trashed an item can then be restored to add it back to
    baserow just as it was when it was trashed.
    """

    name = "trashable"


trash_item_type_registry = TrashableItemTypeRegistry()


class TrashableItemType(ModelInstanceMixin, Instance, ABC):
    """
    A TrashableItemType specifies a baserow model which can be trashed.
    """

    def lookup_trashed_item(self, trashed_item_id: int):
        """
        Returns the actual instance of the trashed item. By default simply does a get
        on the model_class's trash manager.

        :param trashed_item_id: The id to lookup.
        :return: An instance of the model_class with trashed_item_id
        """

        return self.model_class.trash.get(id=trashed_item_id)

    @abstractmethod
    def permanently_delete_item(self, trashed_item: Any):
        """
        Should be implemented to actually delete the specified trashed item from the
        database and do any other required clean-up.

        :param trashed_item: The item to delete permanently.
        """
        pass

    @abstractmethod
    def trashed_item_restored(self, trashed_item: Any):
        """
        Called when a trashed item is restored, should perform any extra operations
        such as sending web socket signals which occur when an item is "created" in
        baserow.

        :param trashed_item: The item that has been restored.
        """
        pass


class GroupTrashableItemType(TrashableItemType):
    def trashed_item_restored(self, trashed_item: Group):
        """
        Informs any clients that the group exists again.
        """

        # TODO Trash - Can't reorder groups after a restore in GUI?
        group_created.send(self, group=trashed_item, user=None)

    def permanently_delete_item(self, trashed_item: Group):
        """
        Deletes the provided group and all of its applications permanently.
        """

        # Select all the applications so we can delete them via the handler which is
        # needed in order to call the pre_delete method for each application.
        applications = trashed_item.application_set.all().select_related("group")
        for application in applications:
            self._delete_application(application)

        trashed_item.delete()

    @staticmethod
    def _delete_application(application):
        """
        Deletes an application and the related relations in the correct way.
        """

        # TODO Dedupe somehow with the application delete code
        application = application.specific
        application_type = application_type_registry.get_by_model(application)
        application_type.pre_delete(application)
        application.delete()
        return application

    type = "group"
    model_class = Group
