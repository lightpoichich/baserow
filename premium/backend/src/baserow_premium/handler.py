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
        print(user)
        if "is_active" in data:
            user.is_active = data["is_active"]
        if "is_staff" in data:
            user.is_staff = data["is_staff"]
        if "username" in data:
            user.username = data["username"]
        if "full_name" in data:
            user.first_name = data["full_name"]
        if "password" in data:
            user.set_password(data["password"])
        user.save()
        return user

    def delete_user(self, user_id):
        user = User.objects.get(id=user_id)
        user.delete()
