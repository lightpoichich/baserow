from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.fields import (
    CharField,
    EmailField,
    DateTimeField,
)
from rest_framework.serializers import ModelSerializer

from baserow.core.models import GroupUser

User = get_user_model()


class AdminGroupUserSerializer(ModelSerializer):
    id = serializers.IntegerField(source="group.id")
    name = serializers.CharField(source="group.name")

    class Meta:
        model = GroupUser

        fields = (
            "id",
            "name",
            "permissions",
        )


class AdminUserSerializer(ModelSerializer):
    # Max length set to match django user models first_name fields max length
    full_name = CharField(source="first_name", max_length=30, required=False)
    username = EmailField(required=False)
    groups = AdminGroupUserSerializer(
        source="groupuser_set", many=True, required=False, read_only=True
    )
    date_joined = DateTimeField(read_only=True)

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
