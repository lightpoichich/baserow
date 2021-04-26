from django.contrib.auth import get_user_model
from rest_framework.fields import CharField, EmailField
from rest_framework.serializers import ModelSerializer

from baserow.api.groups.serializers import GroupSerializer

User = get_user_model()


class PartialAdminUserSerializer(ModelSerializer):
    full_name = CharField(source="first_name", required=False, max_length=30)
    username = EmailField(required=False)
    groups = GroupSerializer(source="group_set", many=True, required=False)

    class Meta:
        model = User
        read_only_fields = ("id", "last_login", "date_joined" "groups")
        fields = (
            "id",
            "username",
            "full_name",
            "groups",
            "last_login",
            "date_joined",
            "is_active",
            "is_staff",
            "password",
        )
        extra_kwargs = {"password": {"write_only": True, "required": False}}
