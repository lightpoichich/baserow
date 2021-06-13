from abc import ABC, abstractmethod
from typing import Any, Optional

from baserow.core.models import Group, Application
from baserow.core.registries import application_type_registry
from baserow.core.registry import (
    ModelRegistryMixin,
    Registry,
    ModelInstanceMixin,
    Instance,
)
from baserow.core.signals import group_created, group_user_updated, application_created


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

    @abstractmethod
    def get_name(self, trashed_item: Any) -> str:
        """
        Should return the name of this particular trashed item to display in the trash
        modal.

        :param trashed_item: The item to be named.
        :return The name of the trashed_group
        """
        pass

    @abstractmethod
    def get_parent_name(self, trashed_item: Any) -> Optional[str]:
        """
        Should return the name of the parent for this particular trashed item to
        display in the trash modal.

        :param trashed_item: The item whose parent is to be named.
        :return The name of the parent of the trashed_group if any or None if no parent.
        """
        pass

    @abstractmethod
    def get_parent_type(self) -> Optional[str]:
        """
        :return The trashable item type of the parent if this type has one.
        """
        pass

    # noinspection PyMethodMayBeStatic
    def get_parent_id(self, trashed_item: Any) -> int:
        """
        :return The item id of the provided trashed_item's parent if this type has one.
        """
        return 0


class GroupTrashableItemType(TrashableItemType):
    def get_parent_type(self) -> Optional[str]:
        return None

    def get_name(self, trashed_item: Group) -> str:
        return trashed_item.name

    def get_parent_name(self, trashed_item: Any) -> Optional[str]:
        return None

    def trashed_item_restored(self, trashed_item: Group):
        """
        Informs any clients that the group exists again.
        """

        # TODO Trash - How does this perform? Do we want to instead provide group
        #  member info in the group_created signal? Without this the front end does
        #  not know what permission they have in the group which breaks things!
        for group_user in trashed_item.groupuser_set.all():
            group_user_updated.send(self, group_user=group_user, user=None)
        group_created.send(self, group=trashed_item, user=None)

    def permanently_delete_item(self, trashed_group: Group):
        """
        Deletes the provided group and all of its applications permanently.
        """

        # Select all the applications so we can delete them via the handler which is
        # needed in order to call the pre_delete method for each application.
        applications = trashed_group.application_set.all().select_related("group")
        application_trashable_type = trash_item_type_registry.get("application")
        for application in applications:
            application_trashable_type.permanently_delete_item(application)

        trashed_group.delete()

    type = "group"
    model_class = Group


class ApplicationTrashableItemType(TrashableItemType):
    def get_name(self, trashed_item: Application) -> str:
        return trashed_item.name

    def get_parent_name(self, trashed_item: Application) -> Optional[str]:
        return trashed_item.group.name

    def trashed_item_restored(self, trashed_item: Application):
        application_created.send(
            self,
            application=trashed_item,
            user=None,
        )

    def permanently_delete_item(self, trashed_item: Application):
        """
        Deletes an application and the related relations in the correct way.
        """

        application = trashed_item.specific
        application_type = application_type_registry.get_by_model(application)
        application_type.pre_delete(application)
        application.delete()
        return application

    def get_parent_type(self) -> Optional[str]:
        return "group"

    def get_parent_id(self, trashed_app) -> int:
        return trashed_app.group.id

    type = "application"
    model_class = Application
