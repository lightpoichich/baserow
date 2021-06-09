from django.apps import AppConfig


class CoreConfig(AppConfig):
    name = "baserow.core"

    def ready(self):
        from baserow.core.trash.registry import trash_item_type_registry
        from baserow.core.trash.registry import GroupTrashableItemType

        trash_item_type_registry.register(GroupTrashableItemType())
