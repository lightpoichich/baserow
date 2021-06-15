from django.utils.functional import lazy
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers, fields

from baserow.api.mixins import UnknownFieldRaisesExceptionSerializerMixin
from baserow.core.models import Trash, Group, Application
from baserow.core.trash.registry import trash_item_type_registry


class TrashStructureApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ("id", "name", "trashed")


class TrashEntryRequestSerializer(
    UnknownFieldRaisesExceptionSerializerMixin, serializers.Serializer
):
    trash_item_id = serializers.IntegerField(min_value=0)
    parent_trash_item_id = serializers.IntegerField(min_value=0, required=False)
    trash_item_type = fields.ChoiceField(
        choices=lazy(trash_item_type_registry.get_types, list)(),
    )


class TrashStructureGroupSerializer(serializers.Serializer):
    id = serializers.IntegerField(min_value=0)
    trashed = serializers.BooleanField()
    name = serializers.CharField()
    applications = TrashStructureApplicationSerializer(many=True)


class TrashContentsGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ("id", "trashed")


class TrashStructureSerializer(serializers.Serializer):
    groups = TrashStructureGroupSerializer(many=True)


class TrashContentsSerializer(serializers.ModelSerializer):
    user_who_trashed = serializers.SerializerMethodField()

    @extend_schema_field(OpenApiTypes.STR)
    def get_user_who_trashed(self, instance):
        if instance.user_who_trashed is not None:
            return instance.user_who_trashed.first_name
        else:
            return None

    class Meta:
        model = Trash
        fields = (
            "id",
            "user_who_trashed",
            "trash_item_type",
            "trash_item_id",
            "parent_trash_item_id",
            "trashed_at",
            "application",
            "group",
            "name",
            "parent_name",
            "extra_description",
        )
