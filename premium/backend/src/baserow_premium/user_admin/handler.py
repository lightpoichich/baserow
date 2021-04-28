from typing import List, Optional

from django.contrib.auth import get_user_model

from baserow_premium.user_admin.exceptions import (
    AdminOnlyOperationException,
    InvalidSortAttributeException,
)

User = get_user_model()


def multi_setattr(obj, attributes):
    for key, value in attributes:
        setattr(obj, key, value)


class Sort:
    def __init__(self, sort_descending: bool, field_name: str):
        self.sort_descending = sort_descending
        self.field_name = field_name


class UserAdminHandler:
    def get_users(
        self, requesting_user: User, username_search: Optional[str], sorts: List[Sort]
    ):
        self.raise_if_not_permitted(requesting_user)
        users = User.objects.all()
        if username_search:
            users = users.filter(username__icontains=username_search)

        users = self.apply_sorts(sorts, users)

        return users

    def apply_sorts(self, sorts, users):
        django_sorts = []
        for sort in sorts:
            sort_prefix = "" if sort.sort_descending else "-"
            if sort.field_name not in self.sortable_user_fields():
                raise InvalidSortAttributeException()

            django_sorts.append(
                f"{sort_prefix}{self.sortable_user_fields()[sort.field_name]}"
            )
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
