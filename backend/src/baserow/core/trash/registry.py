from abc import ABC, abstractmethod
from typing import Any, Optional, List

from baserow.core.models import Group, Application, Trash
from baserow.core.registries import application_type_registry
from baserow.core.registry import (
    ModelRegistryMixin,
    Registry,
    ModelInstanceMixin,
    Instance,
)
from baserow.core.signals import (
    application_created,
    group_restored,
)


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

    def lookup_trashed_item(self, trashed_entry: Trash):
        """
        Returns the actual instance of the trashed item. By default simply does a get
        on the model_class's trash manager.

        :param trashed_entry: The entry to get the real trashed instance for.
        :return: An instance of the model_class with trashed_item_id
        """

        return self.model_class.trash.get(id=trashed_entry.trash_item_id)

    @abstractmethod
    def permanently_delete_item(self, trashed_item: Any):
        """
        Should be implemented to actually delete the specified trashed item from the
        database and do any other required clean-up.

        :param trashed_item: The item to delete permanently.
        """
        pass

    @abstractmethod
    def trashed_item_restored(self, trashed_item: Any, trash_entry: Trash):
        """
        Called when a trashed item is restored, should perform any extra operations
        such as sending web socket signals which occur when an item is "created" in
        baserow.

        :param trash_entry: The trash entry that was restored from.
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
    def get_parent_name(
        self, trashed_item: Any, parent_id: Optional[int]
    ) -> Optional[str]:
        """
        Should return the name of the parent for this particular trashed item to
        display in the trash modal.

        :param trashed_item: The item whose parent is to be named.
        :param parent_id: The id of the parent item if it exists.
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
        :return The item id of the provided trashed_entry's parent if this type has one.
        """
        return 0

    # noinspection PyMethodMayBeStatic
    def get_items_to_trash(
        self, trashed_item: Any, parent_id: Optional[int]
    ) -> List[Any]:
        """
        When trashing some items you might also need to mark other related items also
        as trashed. Override this method and return instances of trashable models
        which should also be marked as trashed. Each of these instances will not
        however be given their own unique trash entry, but instead be restored
        all together from a single trash entry made for trashed_item only.

        :return  An iterable of trashable model instances.
        """
        return [trashed_item]

    # noinspection PyMethodMayBeStatic
    def get_extra_description(self, trashed_item: Any, parent_id: int) -> Optional[str]:
        """
        Should return an optional extra description to show along with the trash
        entry for this particular trashed item.

        :return A short string giving extra detail on what has been trashed.
        """
        return None


class GroupTrashableItemType(TrashableItemType):
    def get_parent_type(self) -> Optional[str]:
        return None

    def get_name(self, trashed_item: Group) -> str:
        return trashed_item.name

    def get_parent_name(
        self, trashed_item: Any, parent_id: Optional[int]
    ) -> Optional[str]:
        return None

    def trashed_item_restored(self, trashed_item: Group, trash_entry: Trash):
        """
        Informs any clients that the group exists again.
        """

        for group_user in trashed_item.groupuser_set.all():
            group_restored.send(self, group_user=group_user, user=None)

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

    def get_parent_name(
        self, trashed_item: Application, parent_id: Optional[int]
    ) -> Optional[str]:
        return trashed_item.group.name

    def trashed_item_restored(self, trashed_item: Application, trash_entry: Trash):
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
