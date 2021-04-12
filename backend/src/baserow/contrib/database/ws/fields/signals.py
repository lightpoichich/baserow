from django.dispatch import receiver
from django.db import transaction

from baserow.ws.registries import page_registry

from baserow.contrib.database.fields import signals as field_signals
from baserow.contrib.database.fields.registries import field_type_registry
from baserow.contrib.database.api.fields.serializers import FieldSerializer


@receiver(field_signals.field_created)
def field_created(sender, field, user, **kwargs):
    table_page_type = page_registry.get("table")
    transaction.on_commit(
        lambda: table_page_type.broadcast(
            {
                "type": "field_created",
                "field": field_type_registry.get_serializer(
                    field, FieldSerializer
                ).data,
            },
            getattr(user, "web_socket_id", None),
            table_id=field.table_id,
        )
    )


@receiver(field_signals.field_updated)
def field_updated(sender, field, user, **kwargs):
    table_page_type = page_registry.get("table")
    transaction.on_commit(
        lambda: table_page_type.broadcast(
            {
                "type": "field_updated",
                "field_id": field.id,
                "field": field_type_registry.get_serializer(
                    field, FieldSerializer
                ).data,
            },
            getattr(user, "web_socket_id", None),
            table_id=field.table_id,
        )
    )


@receiver(field_signals.field_deleted)
def field_deleted(sender, field_id, field, user, **kwargs):
    table_page_type = page_registry.get("table")
    transaction.on_commit(
        lambda: table_page_type.broadcast(
            {"type": "field_deleted", "table_id": field.table_id, "field_id": field_id},
            getattr(user, "web_socket_id", None),
            table_id=field.table_id,
        )
    )
