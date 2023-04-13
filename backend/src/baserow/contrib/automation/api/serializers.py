from baserow.api.applications.serializers import ApplicationSerializer


class AutomationSerializer(ApplicationSerializer):
    class Meta(ApplicationSerializer.Meta):
        ref_name = "AutomationApplication"
        # fields = ApplicationSerializer.Meta.fields + ()
