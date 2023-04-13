from baserow.core.registries import ConnectionType

from .models import ExternalBaserowConnection, InternalBaserowConnection


class InternalBaserowConnectionType(ConnectionType):
    type = "internal_baserow"
    model_class = InternalBaserowConnection

    def enhance_queryset(self, queryset):
        return queryset.select_related("authorized_user")


class ExternalBaserowConnectionType(ConnectionType):
    type = "external_baserow"
    model_class = ExternalBaserowConnection
