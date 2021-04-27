from django.contrib.auth import get_user_model

from baserow_premium.user_admin.exceptions import AdminOnlyOperationException

User = get_user_model()


def multi_setattr(obj, attributes):
    for key, value in attributes:
        setattr(obj, key, value)


class UserAdminHandler:
    def get_users(self, requesting_user):
        self.raise_if_not_permitted(requesting_user)
        return User.objects.order_by("id").all()

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
