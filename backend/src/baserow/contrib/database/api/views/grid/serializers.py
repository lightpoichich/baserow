from rest_framework import serializers

from baserow.contrib.database.views.models import GridViewFieldOptions


class GridViewFieldOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = GridViewFieldOptions
        fields = ("width", "hidden", "order")


class GridViewFilterSerializer(serializers.Serializer):
    field_ids = serializers.ListField(
        allow_empty=True,
        allow_null=True,
        required=False,
        default=None,
        child=serializers.IntegerField(),
        help_text="Only the fields related to the provided ids are added to the "
        "response. If None are provided then all fields will be provided unless "
        "`field_names` is provided which will then filter the returned "
        "fields.",
    )
    field_names = serializers.ListField(
        allow_empty=True,
        allow_null=True,
        required=False,
        default=None,
        child=serializers.CharField(),
        help_text="Only the fields related to the provided names are added to the "
        "response. If None are provided all fields will be returned unless `field_ids` "
        "is provided which will then filter the returned fields.",
    )
    row_ids = serializers.ListField(
        allow_empty=False,
        child=serializers.IntegerField(),
        help_text="Only rows related to the provided ids are added to the response.",
    )
