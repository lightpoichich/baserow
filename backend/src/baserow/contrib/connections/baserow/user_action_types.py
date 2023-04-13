from baserow.core.registries import UserActionType
from baserow.core.handler import CoreHandler

from baserow.contrib.database.rows.operations import ReadDatabaseRowOperationType
from baserow.contrib.database.api.rows.serializers import (
    RowSerializer,
    get_row_serializer_class,
)

from .models import BaserowListRowsUserAction, BaserowGetRowUserAction
from .connection_types import InternalBaserowConnectionType


class BaserowListRowsUserActionType(UserActionType):
    connection_type = InternalBaserowConnectionType.type
    type = "baserow_list_rows"
    model_class = BaserowListRowsUserAction

    def dispatch(self, instance):
        table = instance.table
        connection = instance.connection

        CoreHandler().check_permissions(
            connection.authorized_user,
            ReadDatabaseRowOperationType.type,
            workspace=table.database.workspace,
            context=table,
            raise_permission_exceptions=True,
        )

        model = instance.table.get_model()
        rows = model.objects.all()[:200]

        serializer = get_row_serializer_class(
            model,
            RowSerializer,
            is_response=True,
            user_field_names=True,
        )
        serialized_rows = serializer(rows, many=True).data

        print('fetched list of rows')
        return serialized_rows


class BaserowGetRowUserActionType(UserActionType):
    connection_type = InternalBaserowConnectionType.type
    type = "baserow_get_row"
    model_class = BaserowGetRowUserAction

    def dispatch(self, instance):
        table = instance.table
        connection = instance.connection

        CoreHandler().check_permissions(
            connection.authorized_user,
            ReadDatabaseRowOperationType.type,
            workspace=table.database.workspace,
            context=table,
            raise_permission_exceptions=True,
        )

        model = instance.table.get_model()
        row = model.objects.get(pk=instance.row_id)

        serializer = get_row_serializer_class(
            model,
            RowSerializer,
            is_response=True,
            user_field_names=True,
        )
        serialized_row = serializer(row).data

        print('fetched single row')
        return serialized_row
