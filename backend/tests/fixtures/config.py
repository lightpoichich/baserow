from baserow.core.models import Config


class ConfigFixtures:
    def update_config(self, **kwargs):
        config, created = Config.objects.update_or_create(defaults=kwargs)
        return config
