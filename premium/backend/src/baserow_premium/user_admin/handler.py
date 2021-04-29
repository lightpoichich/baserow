from typing import List, Optional

from django.contrib.auth import get_user_model

from baserow_premium.user_admin.exceptions import (
    AdminOnlyOperationException,
)

from enum import Enum, unique

User = get_user_model()


@unique
class SortableUserAdminField(Enum):
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


def multi_setattr(obj, attributes):
    for key, value in attributes:
        setattr(obj, key, value)


class UserAdminSort:
    """
    A simple value class indicating how to sort a particular user admin field.
    """

    def __init__(self, sort_descending: bool, field_name: SortableUserAdminField):
        """"""
        self.sort_descending = sort_descending
        self.field_name = field_name


class UserAdminHandler:
    def get_users(
        self,
        requesting_user: User,
        username_search: Optional[str] = None,
        sorts: Optional[List[UserAdminSort]] = None,
    ):
        self.raise_if_not_permitted(requesting_user)

        users = User.objects.all()
        if username_search is not None:
            users = users.filter(username__icontains=username_search)

        if sorts is None:
            sorts = []
        users = self.apply_sorts(sorts, users)

        return users

    @staticmethod
    def apply_sorts(sorts: List[UserAdminSort], users):
        django_sorts = []
        for sort in sorts:
            sort_prefix = "" if sort.sort_descending else "-"

            sort_db_column = sort.field_name.underlying_user_database_column_name()
            django_sorts.append(f"{sort_prefix}{sort_db_column}")
        if django_sorts:
            users = users.order_by(*django_sorts)
        else:
            users = users.order_by("id")
        return users

    @staticmethod
    def sortable_user_fields():
        return {
            "id": "id",
            "is_active": "is_active",
            "username": "username",
            "full_name": "first_name",
            "date_joined": "date_joined",
            "last_login": "last_login",
        }

    @staticmethod
    def editable_user_fields():
        return [
            ("is_active", setattr),
            ("is_staff", setattr),
            (
                "username",
                lambda user, _, username: multi_setattr(
                    user, [("username", username), ("email", username)]
                ),
            ),
            (
                "full_name",
                lambda user, _, full_name: setattr(user, "first_name", full_name),
            ),
            ("password", lambda user, _, password: user.set_password(password)),
        ]

    def update_user(self, requesting_user, user_id, data):
        self.raise_if_not_permitted(requesting_user)

        user = User.objects.get(id=user_id)
        for field_name, setattr_func in self.editable_user_fields():
            if field_name in data:
                setattr_func(user, field_name, data[field_name])
        user.save()
        return user

    def delete_user(self, requesting_user, user_id):
        self.raise_if_not_permitted(requesting_user)

        user = User.objects.get(id=user_id)
        user.delete()

    @staticmethod
    def raise_if_not_permitted(requesting_user):
        if not requesting_user.is_staff:
            raise AdminOnlyOperationException()
