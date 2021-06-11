from rest_framework import serializers

from baserow.core.models import Trash, Group, Application


class TrashStructureApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = (
            "id",
            "name"
            # TODO Trash - Remove when apps are trashable "trashed"
        )


class TrashStructureGroupSerializer(serializers.ModelSerializer):
    applications = TrashStructureApplicationSerializer(
        source="application_set", many=True
    )

    class Meta:
        model = Group
        fields = ("id", "trashed", "name", "applications")


class TrashContentsGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ("id", "trashed")


class TrashStructureSerializer(serializers.Serializer):
    groups = TrashStructureGroupSerializer(many=True)


class TrashContentsSerializer(serializers.ModelSerializer):
    user_who_trashed = serializers.CharField(
        source="user_who_trashed.first_name", max_length=32
    )

    class Meta:
        model = Trash
        fields = (
            "id",
            "user_who_trashed",
            "trash_item_type",
            "trash_item_id",
            "trashed_at",
            "application",
            "group",
            "name",
            "parent_name",
        )
