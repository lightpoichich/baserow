from baserow.core.models import Settings


class SettingsFixtures:
    def update_settings(self, **kwargs):
        config, created = Settings.objects.update_or_create(defaults=kwargs)
        return config
