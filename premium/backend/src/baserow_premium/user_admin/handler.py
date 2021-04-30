from typing import List, Optional, Any, Dict

from django.contrib.auth import get_user_model

from baserow_premium.user_admin.exceptions import (
    AdminOnlyOperationException,
    CannotDeactivateYourselfException,
    CannotDeleteYourselfException,
)

from enum import Enum, unique

User = get_user_model()


@unique
class SortableUserAdminField(Enum):
    """
    The various attributes for which users returned by the UserAdminHandler can be
    sorted.
    """

    ID = "id"
    IS_ACTIVE = "is_active"
    USERNAME = "username"
    FULL_NAME = "full_name"
    DATE_JOINED = "date_joined"
    LAST_LOGIN = "last_login"

    def underlying_user_database_column_name(self):
        if self == SortableUserAdminField.FULL_NAME:
            return "first_name"
        else:
            return self.value


@unique
class UserAdminSortDirection(Enum):
    """
    The directions in which user attributes can be sorted by the UserAdminHandler.
    """

    DESC = "+"
    ASC = "-"

    def to_django_sort_prefix(self) -> str:
        """
        :return: The prefix used by django's order_by method to achieve the desired sort
                 direction.
        """
        if self == UserAdminSortDirection.DESC:
            return ""
        else:
            return "-"


@unique
class EditableUserAdminField(Enum):
    """
    The various user attributes which can be updated for a given use by the
    UserAdminHandler.
    """

    IS_ACTIVE = "is_active"
    IS_STAFF = "is_staff"
    USERNAME = "username"
    FULL_NAME = "full_name"
    PASSWORD = "password"

    def edit_user(self, requesting_user, user, new_value):
        """
        Performs the correct user update operation for a given UserAdminField.
        Raises an exception if the requesting user is attempting to de-activate or
        un-staff themselves.
        """
        if self == EditableUserAdminField.FULL_NAME:
            user.first_name = new_value
        elif self == EditableUserAdminField.USERNAME:
            user.username = new_value
            user.email = new_value
        elif self == EditableUserAdminField.PASSWORD:
            user.set_password(new_value)
        elif (
            self in [EditableUserAdminField.IS_ACTIVE, EditableUserAdminField.IS_STAFF]
            and not new_value
            and requesting_user == user
        ):
            raise CannotDeactivateYourselfException()
        else:
            setattr(user, self.value, new_value)

        return user


class UserAdminSort:
    """
    A simple value class indicating how to sort a particular user admin field.
    """

    def __init__(
        self, direction: UserAdminSortDirection, field_name: SortableUserAdminField
    ):
        """"""
        self.direction = direction
        self.field_name = field_name


class UserAdminHandler:
    def get_users(
        self,
        requesting_user: User,
        username_search: Optional[str] = None,
        sorts: Optional[List[UserAdminSort]] = None,
    ):
        """
        Looks up all users, performs an optional username search and then sorts the
        resulting user queryset and returns it. By default if no sorts are provided
        sorts by user id ascending.

        :param requesting_user: The user who is making the request to get_users, the
                                user must be a staff member or else an exception will
                                be raised.
        :param username_search: An optional icontains username search to filter the
                                returned users by.
        :param sorts: A list of sorts to be applied in order over the returned users.
        :return: A queryset of users in Baserow, optionally sorted and ordered by the
                 specified parameters.
        """
        self._raise_if_not_permitted(requesting_user)

        users = User.objects.prefetch_related(
            "groupuser_set", "groupuser_set__group"
        ).all()
        if username_search is not None:
            users = users.filter(username__icontains=username_search)

        if sorts is None:
            sorts = []
        users = self._apply_sorts_or_default_sort(sorts, users)

        return users

    @staticmethod
    def _apply_sorts_or_default_sort(sorts: List[UserAdminSort], users):
        """
        Takes a list of UserAdminSorts and applies them to a django queryset in order.
        Defaults to sorting by user id if no sorts are provided.

        :param sorts: The list of sorts to apply to the users queryset
        :param users: The users queryset to sort
        :return:
        """
        django_sorts = []
        for sort in sorts:
            sort_prefix = sort.direction.to_django_sort_prefix()

            sort_db_column = sort.field_name.underlying_user_database_column_name()
            django_sorts.append(f"{sort_prefix}{sort_db_column}")
        if django_sorts:
            users = users.order_by(*django_sorts)
        else:
            users = users.order_by("id")
        return users

    def update_user(
        self,
        requesting_user: User,
        user_id: int,
        data: Dict[EditableUserAdminField, Any],
    ):
        """
        Updates a specified user with new attribute values. Will raise an exception
        if a user attempts to de-activate or un-staff themselves.

        :param requesting_user: The user who is making the request to update a user, the
                                user must be a staff member or else an exception will
                                be raised.
        :param user_id: The id of the user to update.
        :param data: The fields and their new values to update.
        :return:
        """
        self._raise_if_not_permitted(requesting_user)

        user = User.objects.get(id=user_id)
        for field, new_value in data.items():
            field.edit_user(requesting_user, user, new_value)
        user.save()
        return user

    def delete_user(self, requesting_user: User, user_id: int):
        """
        Deletes a specified user, raises an exception if you attempt to delete yourself.

        :param requesting_user: The user who is making the delete request , the
                                user must be a staff member or else an exception will
                                be raised.
        :param user_id: The id of the user to delete.
        """
        self._raise_if_not_permitted(requesting_user)

        if requesting_user.id == user_id:
            raise CannotDeleteYourselfException()

        user = User.objects.get(id=user_id)
        user.delete()

    @staticmethod
    def _raise_if_not_permitted(requesting_user):
        if not requesting_user.is_staff:
            raise AdminOnlyOperationException()
