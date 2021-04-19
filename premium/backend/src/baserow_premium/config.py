from django.apps import AppConfig

from baserow.core.registries import plugin_registry


class BaserowPremiumConfig(AppConfig):
    name = "baserow_premium"

    def ready(self):
        from .plugins import PremiumPlugin

        plugin_registry.register(PremiumPlugin())
