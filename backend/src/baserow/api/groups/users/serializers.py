from django.contrib.auth import get_user_model

from rest_framework import serializers

from baserow.core.models import GroupUser


User = get_user_model()


class GroupUserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()

    class Meta:
        model = GroupUser
        fields = ('name', 'email', 'group', 'permissions', 'created_on')

    def get_name(self, object):
        return object.user.first_name

    def get_email(self, object):
        return object.user.email


class GroupUserGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupUser
        fields = ('order', 'permissions')

    def to_representation(self, instance):
        from baserow.api.groups.serializers import GroupSerializer

        data = super().to_representation(instance)
        data.update(GroupSerializer(instance.group).data)
        return data


class UpdateGroupUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupUser
        fields = ('permissions',)
