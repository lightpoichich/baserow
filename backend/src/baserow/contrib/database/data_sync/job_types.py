from rest_framework import serializers

from baserow.api.errors import ERROR_USER_NOT_IN_GROUP
from baserow.contrib.database.api.data_sync.errors import (
    ERROR_DATA_SYNC_DOES_NOT_EXIST,
    ERROR_SYNC_DATA_SYNC_ALREADY_RUNNING,
)
from baserow.contrib.database.api.data_sync.serializers import DataSyncSerializer
from baserow.contrib.database.data_sync.exceptions import (
    DataSyncDoesNotExist,
    SyncDataSyncTableAlreadyRunning,
)
from baserow.contrib.database.db.atomic import (
    read_repeatable_read_single_table_transaction,
)
from baserow.contrib.database.table.models import DuplicateTableJob
from baserow.core.action.registries import action_type_registry
from baserow.core.exceptions import UserNotInWorkspace
from baserow.core.handler import CoreHandler
from baserow.core.jobs.registries import JobType

from .actions import SyncDataSyncTableActionType
from .handler import DataSyncHandler
from .models import SyncDataSyncTableJob
from .operations import SyncTableOperationType


class SyncDataSyncTableJobType(JobType):
    type = "sync_data_sync_table"
    model_class = SyncDataSyncTableJob
    max_count = 1

    api_exceptions_map = {
        DataSyncDoesNotExist: ERROR_DATA_SYNC_DOES_NOT_EXIST,
        SyncDataSyncTableAlreadyRunning: ERROR_SYNC_DATA_SYNC_ALREADY_RUNNING,
    }
    job_exceptions_map = {
        UserNotInWorkspace: ERROR_USER_NOT_IN_GROUP,
        SyncDataSyncTableAlreadyRunning: ERROR_SYNC_DATA_SYNC_ALREADY_RUNNING[2],
    }
    request_serializer_field_names = ["data_sync_id"]
    request_serializer_field_overrides = {
        "data_sync_id": serializers.IntegerField(
            help_text="The ID of data sync to sync.",
        ),
    }
    serializer_field_names = ["data_sync"]
    serializer_field_overrides = {
        "data_sync": DataSyncSerializer(read_only=True),
    }

    def transaction_atomic_context(self, job: "DuplicateTableJob"):
        return read_repeatable_read_single_table_transaction(job.data_sync.table_id)

    def prepare_values(self, values, user):
        data_sync = DataSyncHandler().get_data_sync(values["data_sync_id"])
        CoreHandler().check_permissions(
            user,
            SyncTableOperationType.type,
            workspace=data_sync.table.database.workspace,
            context=data_sync.table,
        )
        return {"data_sync": data_sync}

    def run(self, job, progress):
        data_sync = job.data_sync.specific
        data_sync = action_type_registry.get_by_type(SyncDataSyncTableActionType).do(
            job.user, data_sync
        )
        progress.set_progress(100)
        return data_sync
