from rest_framework import serializers

from drf_spectacular.utils import extend_schema_field

from baserow.api.user_files.serializers import UserFileField
from baserow.contrib.database.api.fields.serializers import FieldSerializer
from baserow.contrib.database.fields.models import Field
from baserow.contrib.database.views.models import FormView, FormViewFieldOptions
from baserow.contrib.database.fields.registries import field_type_registry


class FormViewFieldOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormViewFieldOptions
        fields = ("name", "description", "enabled", "required", "order")


class PublicFormViewFieldSerializer(FieldSerializer):
    class Meta:
        model = Field
        fields = ("type",)


class PublicFormViewFieldOptionsSerializer(FieldSerializer):
    field = serializers.SerializerMethodField()

    class Meta:
        model = FormViewFieldOptions
        fields = ("name", "description", "required", "order", "field")

    # @TODO show correct API docs.
    @extend_schema_field(PublicFormViewFieldSerializer)
    def get_field(self, instance):
        return field_type_registry.get_serializer(
            instance.field, PublicFormViewFieldSerializer
        ).data


class PublicFormViewSerializer(serializers.ModelSerializer):
    title = serializers.CharField()
    description = serializers.CharField()
    cover_image = UserFileField()
    logo_image = UserFileField()
    fields = PublicFormViewFieldOptionsSerializer(
        many=True, source="active_field_options"
    )

    class Meta:
        model = FormView
        fields = ("title", "description", "cover_image", "logo_image", "fields")


class FormViewSubmittedSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormView
        fields = (
            "submit_action",
            "submit_action_message",
            "submit_action_redirect_url",
        )
