from rest_framework import serializers

from baserow.core.models import Trash, Group, Application


class TrashStructureApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = (
            "id",
            # TODO Trash - Remove when apps are trashable "trashed"
        )


class TrashStructureGroupSerializer(serializers.ModelSerializer):
    applications = TrashStructureApplicationSerializer(
        source="application_set", many=True
    )

    class Meta:
        model = Group
        fields = ("id", "trashed", "applications")


class TrashContentsGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ("id", "trashed")


class TrashStructureSerializer(serializers.Serializer):
    groups = TrashStructureGroupSerializer(many=True)


class TrashContentsSerializer(serializers.ModelSerializer):
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
        )
