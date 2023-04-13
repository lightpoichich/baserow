from baserow.contrib.automation.trigger_types import SignalViaTaskTriggerType
from baserow.contrib.database.api.rows.serializers import (
    RowSerializer,
    get_row_serializer_class,
)
from baserow.contrib.database.rows.operations import ReadDatabaseRowOperationType
from baserow.contrib.database.rows.signals import rows_created
from baserow.contrib.database.table.handler import TableDoesNotExist, TableHandler
from baserow.core.handler import CoreHandler

from .connection_types import InternalBaserowConnectionType
from .models import BaserowRowCreatedTrigger


class BaserowRowsCreatedTriggerType(SignalViaTaskTriggerType):
    type = "baserow_rows_created"
    model_class = BaserowRowCreatedTrigger
    connection_type = InternalBaserowConnectionType.type
    signal = rows_created

    def get_test_kwargs(self, trigger):
        print("@TODO construct a serialized row based on the table.")
        return {"table_id": trigger.table_id, "rows": []}

    def prepare_signal_kwargs_for_task(self, table, model, rows, **kwargs):
        serializer = get_row_serializer_class(
            model,
            RowSerializer,
            is_response=True,
            user_field_names=True,
        )
        created_rows = serializer(rows, many=True).data
        return {"table_id": table.id, "rows": created_rows}

    def enhance_find_triggers_queryset(self, queryset, table_id, **kwargs):
        return queryset.filter(table_id=table_id)

    def prepare_runs(self, triggers, **kwargs):
        runs = super().prepare_runs(triggers, **kwargs)

        try:
            table = TableHandler().get_table(kwargs["table_id"])
            for index, run in enumerate(runs):
                trigger = triggers[index]
                check = CoreHandler().check_permissions(
                    trigger.connection.authorized_user,
                    ReadDatabaseRowOperationType.type,
                    workspace=table.database.workspace,
                    context=table,
                    raise_permission_exceptions=False,
                )

                if not check:
                    run.fail(
                        "Authorized user doesn't have read permissions to the table."
                    )
        except TableDoesNotExist:
            for run in runs:
                run.fail("Table does not exist.")

        return runs

    def get_payload(self, trigger, **kwargs):
        return kwargs["rows"]
