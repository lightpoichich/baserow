from rest_framework import serializers

from baserow.contrib.database.views.models import FormViewFieldOptions


class FormViewFieldOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormViewFieldOptions
        fields = ("name", "description", "enabled", "required", "order")
