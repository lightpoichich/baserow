from baserow.core.models import Settings


class ConfigFixtures:
    def update_settings(self, **kwargs):
        config, created = Settings.objects.update_or_create(defaults=kwargs)
        return config
