from django.dispatch import receiver
from django.db import transaction

from baserow.ws.registries import page_registry

from baserow.contrib.database.views import signals as view_signals
from baserow.contrib.database.views.registries import view_type_registry
from baserow.contrib.database.api.views.serializers import ViewSerializer


@receiver(view_signals.view_created)
def view_created(sender, view, user, **kwargs):
    table_page_type = page_registry.get('table')
    transaction.on_commit(lambda: table_page_type.broadcast(
        {
            'type': 'view_created',
            'view': view_type_registry.get_serializer(view, ViewSerializer).data
        },
        getattr(user, 'web_socket_id', None),
        table_id=view.table_id
    ))


@receiver(view_signals.view_updated)
def view_updated(sender, view, user, **kwargs):
    table_page_type = page_registry.get('table')
    transaction.on_commit(lambda: table_page_type.broadcast(
        {
            'type': 'view_updated',
            'view_id': view.id,
            'view': view_type_registry.get_serializer(view, ViewSerializer).data
        },
        getattr(user, 'web_socket_id', None),
        table_id=view.table_id
    ))


@receiver(view_signals.view_deleted)
def view_deleted(sender, view_id, view, user, **kwargs):
    table_page_type = page_registry.get('table')
    transaction.on_commit(lambda: table_page_type.broadcast(
        {
            'type': 'view_deleted',
            'view_id': view_id
        },
        getattr(user, 'web_socket_id', None),
        table_id=view.table_id
    ))
