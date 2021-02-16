from rest_framework import serializers

from baserow.core.models import Config


class ConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = Config
        fields = ('allow_new_signups',)
        extra_kwargs = {
            'allow_new_signups': {'required': False},
        }
