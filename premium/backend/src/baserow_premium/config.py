from django.apps import AppConfig


class BaserowPremiumConfig(AppConfig):
    name = "baserow_premium"

    def ready(self):
        from .plugins import PremiumPlugin
        from baserow.core.registries import plugin_registry

        plugin_registry.register(PremiumPlugin())
