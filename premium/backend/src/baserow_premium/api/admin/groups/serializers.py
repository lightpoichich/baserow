from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from baserow.core.models import Group, GroupUser


User = get_user_model()


class AdminGroupUserSerializer(ModelSerializer):
    id = serializers.IntegerField(source="user.id")
    email = serializers.CharField(source="user.email")

    class Meta:
        model = GroupUser

        fields = ("id", "email", "permissions")


class GroupsAdminResponseSerializer(ModelSerializer):
    users = AdminGroupUserSerializer(source="groupuser_set", many=True)
    application_count = serializers.IntegerField()

    class Meta:
        model = Group
        fields = (
            "id",
            "name",
            "users",
            "application_count",
            "created_on",
        )
