from django.contrib.auth import get_user_model

User = get_user_model()


class PremiumHandler:
    def get_users(
        self,
    ):
        """"""

        query = User.objects.all()

        return query
