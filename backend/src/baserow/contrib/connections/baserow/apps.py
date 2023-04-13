from django.apps import AppConfig


class ConnectionsConfig(AppConfig):
    name = "baserow.contrib.connections.baserow"

    def ready(self) -> None:
        from baserow.contrib.automation.registries import trigger_registry
        from baserow.core.registries import (
            connection_type_registry,
            user_action_type_registry,
        )

        from .connection_types import (
            ExternalBaserowConnectionType,
            InternalBaserowConnectionType,
        )
        from .trigger_types import BaserowRowsCreatedTriggerType
        from .user_action_types import BaserowListRowsUserActionType, \
            BaserowGetRowUserActionType

        connection_type_registry.register(InternalBaserowConnectionType())
        connection_type_registry.register(ExternalBaserowConnectionType())
        user_action_type_registry.register(BaserowListRowsUserActionType())
        user_action_type_registry.register(BaserowGetRowUserActionType())
        trigger_registry.register(BaserowRowsCreatedTriggerType())
