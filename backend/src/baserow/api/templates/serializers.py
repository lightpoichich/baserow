from rest_framework import serializers

from baserow.core.models import TemplateCategory, Template


class TemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Template
        fields = ('id', 'name', 'icon', 'keywords', 'group_id')


class TemplateCategoriesSerializer(serializers.ModelSerializer):
    templates = TemplateSerializer(read_only=True, many=True)

    class Meta:
        model = TemplateCategory
        fields = ('id', 'name', 'templates')
