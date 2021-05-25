from django.apps import AppConfig


class BaserowPremiumConfig(AppConfig):
    name = "baserow_premium"

    def ready(self):
        from baserow.core.registries import plugin_registry
        from baserow.contrib.database.export.registries import table_exporter_registry

        from .plugins import PremiumPlugin

        plugin_registry.register(PremiumPlugin())

        from .export.exporter_types import JSONTableExporter, XMLTableExporter

        table_exporter_registry.register(JSONTableExporter())
        table_exporter_registry.register(XMLTableExporter())
