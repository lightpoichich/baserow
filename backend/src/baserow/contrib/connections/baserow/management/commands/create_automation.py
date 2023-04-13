# Ignoring as only exception imported here so no security issue specifically here

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from baserow.contrib.automation.models import Automation, AutomationRun, Trigger, UserAction
from baserow.contrib.automation.registries import trigger_registry, user_action_type_registry
from baserow.core.db import specific_iterator
from baserow.core.models import Connection
from baserow.core.registries import connection_type_registry

User = get_user_model()


class Command(BaseCommand):
    def handle(self, *args, **options):
        AutomationRun.objects.all().delete()
        for connection in specific_iterator(Connection.objects.all()):
            connection.delete()
        for trigger in specific_iterator(Trigger.objects.all()):
            trigger.delete()
        for action in specific_iterator(UserAction.objects.all()):
            action.delete()
        Automation.objects.all().delete()

        user = User.objects.get(pk=1)

        automation = Automation.objects.create(
            workspace_id=1, name="Tmp Automation", order=10
        )

        baserow_connection_type = connection_type_registry.get("internal_baserow")
        baserow_connection = baserow_connection_type.model_class.objects.create(
            application=automation, name="Baserow Connection", authorized_user=user
        )

        baserow_rows_created_trigger_type = trigger_registry.get("baserow_rows_created")
        baserow_rows_created_trigger = (
            baserow_rows_created_trigger_type.model_class.objects.create(
                connection=baserow_connection, table_id=1
            )
        )

        automation.trigger = baserow_rows_created_trigger
        automation.save()

        baserow_list_rows_user_action_type = user_action_type_registry.get("baserow_list_rows")
        baserow_list_rows_user_action = (
            baserow_list_rows_user_action_type.model_class.objects.create(
                automation=automation, connection=baserow_connection, table_id=1
            )
        )

        baserow_get_row_user_action_type = user_action_type_registry.get(
            "baserow_get_row"
        )
        baserow_get_row_user_action = (
            baserow_get_row_user_action_type.model_class.objects.create(
                automation=automation,
                connection=baserow_connection,
                table_id=1,
                row_id=1,
                parent=baserow_list_rows_user_action,
            )
        )
