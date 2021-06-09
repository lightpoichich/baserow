from typing import Optional, Dict, Any

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import transaction
from django.utils import timezone

from baserow.core.exceptions import (
    ApplicationNotInGroup,
    GroupDoesNotExist,
    ApplicationDoesNotExist,
    TrashItemDoesNotExist,
)
from baserow.core.models import Trash, Application, Group
from baserow.core.trash.registry import trash_item_type_registry

User = get_user_model()


class TrashHandler:
    @staticmethod
    def trash(
        requesting_user: User,
        group: Group,
        application: Optional[Application],
        trash_item,
    ) -> Trash:
        """
        Marks the provided trashable item as trashed meaning it will no longer be
        visible or usable in Baserow. However any user with access to its group can
        restore the item after it is trashed to make it visible and usable again. After
        a configurable timeout period or when the a user explicitly empties the
        trash trashed items will be permanently deleted.

        :param requesting_user: The user who is requesting that this item be trashed.
        :param group: The group the trashed item is in.
        :param application: If the item is in an application the application.
        :param trash_item: The item to be trashed.
        :return: A newly created entry in the Trash table for this item.
        """

        trash_item.trashed = True
        trash_item.save()

        trash_item_type = trash_item_type_registry.get_by_model(trash_item)

        return Trash.objects.create(
            user_who_trashed=requesting_user,
            group=group,
            application=application,
            trash_item_type=trash_item_type.type,
            trash_item_id=trash_item.id,
        )

    @staticmethod
    def restore_item(user, trash_item_type, trash_item_id):
        """
        Restores an item from the trash re-instating it back in Baserow exactly how it
        was before it was trashed.
        :param user: The user requesting to restore trashed item.
        :param trash_item_type: The trashable item type of the item to restore.
        :param trash_item_id: The trash item id of the item to restore.
        :return:
        """

        with transaction.atomic():
            trash_entry = TrashHandler.get_trash_entry(
                user, trash_item_type, trash_item_id
            )

            trashable_item_type = trash_item_type_registry.get(
                trash_entry.trash_item_type
            )
            trashed_item = trashable_item_type.lookup_trashed_item(
                trash_entry.trash_item_id
            )

            trashed_item.trashed = False
            trashed_item.save()
            Trash.objects.filter(
                trash_item_type=trash_item_type, trash_item_id=trashed_item.id
            ).delete()

            trashable_item_type.trashed_item_restored(trashed_item)

    @staticmethod
    def get_trash_entry(user, trash_item_type, trash_item_id):
        try:
            trash_entry = Trash.objects.get(
                trash_item_id=trash_item_id, trash_item_type=trash_item_type
            )
        except Trash.DoesNotExist:
            raise TrashItemDoesNotExist()
        trash_entry.group.has_user(user, raise_error=True, include_trash=True)
        return trash_entry

    @staticmethod
    def get_trash_structure(user: User) -> Dict[str, Any]:
        """
        Returns the structure of the trash available to the user. This consists of the
        groups and their applications the user has access to. Each group and application
        indicates whether it itself has been trashed.

        :param user: The user to return the trash structure for.
        :return: An ordered list of groups and their applications which could possibly
            have trash contents.
        """
        groups = Group.objects_and_trash.filter(groupuser__user=user)
        perm_deleted_groups = Trash.objects.filter(
            trash_item_type="group",
            should_be_permanently_deleted=True,
            trash_item_id__in=groups.values_list("id", flat=True),
        ).values_list("trash_item_id", flat=True)
        return {
            "groups": (
                groups.exclude(id__in=perm_deleted_groups).order_by("groupuser__order")
            )
        }

    @staticmethod
    def mark_old_trash_for_permanent_deletion():
        """
        Updates all trash entries which are older than a django setting for permanent
        deletion. Does not perform the deletion itself.
        """
        now = timezone.now()
        cutoff = now - timezone.timedelta(
            hours=settings.HOUR_DURATION_UNTIL_TRASH_ITEM_PERMANENTLY_DELETED
        )
        Trash.objects.filter(trashed_at__lte=cutoff).update(
            should_be_permanently_deleted=True
        )

    @staticmethod
    def empty(requesting_user: User, group_id: int, application_id: Optional[int]):
        """
        Marks all items in the selected group (or application in the group if
        application_id is provided) as should be permanently deleted.
        """
        with transaction.atomic():
            trash_contents = TrashHandler.get_trash_contents(
                requesting_user, group_id, application_id
            )
            trash_contents.update(should_be_permanently_deleted=True)

    @staticmethod
    def permanently_delete_marked_trash():
        """
        Looks up every trash item marked for permanent deletion and removes them
        irreversibly from the database along with their corresponding trash entries.
        """
        for trash_entry in Trash.objects.filter(should_be_permanently_deleted=True):
            with transaction.atomic():
                trash_item_type = trash_item_type_registry.get(
                    trash_entry.trash_item_type
                )
                to_delete = trash_item_type.lookup_trashed_item(
                    trash_entry.trash_item_id
                )
                trash_item_type.permanently_delete_item(to_delete)
                trash_entry.delete()

    @staticmethod
    def permanently_delete(trashable_item):
        """
        Actually removes the provided trashable item from the database irreversibly.
        :param trashable_item: An instance of a TrashableItemType model_class to delete.
        """
        trash_item_type = trash_item_type_registry.get_by_model(trashable_item)
        trash_item_type.permanently_delete_item(trashable_item)

    @staticmethod
    def get_trash_contents(
        user: User, group_id: int, application_id: Optional[int]
    ) -> Dict[str, Any]:
        """
        Looks up the trash contents for a particular group optionally filtered by
        the provided application id.
        :param user:
        :param group_id:
        :param application_id:
        :raises GroupDoesNotExist: If the group_id is for an non
            existent group.
        :raises ApplicationDoesNotExist: If the application_id is for an non
            existent application.
        :raises ApplicationNotInGroup: If the application_id is for an application
            not in the requested group.
        :raises UserNotInGroup: If the user does not belong to the group.
        :return: a queryset of the trash items in the group optionally filtered by
            the provided application.
        """

        try:
            group = Group.objects_and_trash.get(id=group_id)
        except Group.DoesNotExist:
            raise GroupDoesNotExist

        try:
            trash_entry = TrashHandler.get_trash_entry(user, "group", group.id)
            if trash_entry.should_be_permanently_deleted:
                raise GroupDoesNotExist
        except TrashItemDoesNotExist:
            pass

        group.has_user(user, raise_error=True, include_trash=True)

        if application_id is not None:
            try:
                # TODO Trash search for trashed applications also
                application = Application.objects.get(id=application_id)
            except Application.DoesNotExist:
                raise ApplicationDoesNotExist()

            if application.group != group:
                raise ApplicationNotInGroup()
        else:
            application = None

        # TODO Trash - Raise 404 if app is marked for perm deletion

        # TODO Trash - Lookup trash contents for group
        return Trash.objects.filter(
            group=group, application=application, should_be_permanently_deleted=False
        )
