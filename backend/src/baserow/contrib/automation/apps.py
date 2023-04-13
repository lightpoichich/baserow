from django.apps import AppConfig


class AutomationConfig(AppConfig):
    name = "baserow.contrib.automation"

    def ready(self) -> None:
        from baserow.core.registries import application_type_registry

        from .application_types import AutomationApplicationType

        application_type_registry.register(AutomationApplicationType())
