from django.contrib.auth import get_user_model

User = get_user_model()


class UserAdminHandler:
    def get_users(
        self,
    ):
        """"""

        return User.objects.order_by("id").all()

    def update_user(self, user_id, data):
        user = User.objects.get(id=user_id)
        user.is_active = data["is_active"]
        user.save()
        return user

    def delete_user(self, user_id):
        user = User.objects.get(id=user_id)
        user.delete()
