from typing import List

from django.contrib.auth.models import AbstractUser

from baserow.contrib.database.db.schema import safe_django_schema_editor
from baserow.contrib.database.operations import CreateTableDatabaseTableOperationType
from baserow.contrib.database.rows.handler import RowHandler
from baserow.contrib.database.search.handler import SearchHandler
from baserow.contrib.database.table.models import Table
from baserow.contrib.database.table.signals import table_created, table_updated
from baserow.core.handler import CoreHandler
from baserow.core.utils import extract_allowed

from .exceptions import PropertyNotFound, UniquePrimaryPropertyNotFound
from .models import DataSync, DataSyncProperty
from .operations import SyncTableOperationType
from .registries import data_sync_type_registry


class DataSyncHandler:
    def create_data_sync_table(
        self,
        user: AbstractUser,
        database,
        type_name,
        visible_properties,
        table_name,
        **kwargs,
    ) -> DataSync:
        """
        Creates a new data sync, the related table, the synced fields, and will
        immediately sync the data.

        :param user: The user on whose behalf the data sync is created.
        :param database: The database where to create the synced table in.
        :param type_name: The type of the data sync that must be created.
        :param visible_properties: A list of data sync property keys that must be added.
            The primary unique ones are always added.
        :param table_name: The name of the synced table that will be created.
        """

        CoreHandler().check_permissions(
            user,
            CreateTableDatabaseTableOperationType.type,
            workspace=database.workspace,
            context=database,
        )

        data_sync_type = data_sync_type_registry.get(type_name)
        model_class = data_sync_type.model_class

        allowed_fields = [] + data_sync_type.allowed_fields
        values = extract_allowed(kwargs, allowed_fields)

        data_sync_instance = model_class(**values)
        data_sync_properties = data_sync_type.get_properties(data_sync_instance)

        # The unique primary properties must always be added to the table because
        # it's used for identification purposes.
        for data_sync_property in data_sync_properties:
            if (
                data_sync_property.unique_primary
                and data_sync_property.key not in visible_properties
            ):
                visible_properties.insert(0, data_sync_property.key)

        # Create an empty table that we're going to sync the data into.
        # @TODO create the table in the `TableHandler` in a reusable way.
        last_order = Table.get_last_order(database)
        table = Table.objects.create(
            database=database,
            order=last_order,
            name=table_name,
            needs_background_update_column_added=True,
        )

        data_sync_instance.table = table
        data_sync_instance.save()

        properties_to_create = []
        has_primary = False
        for index, visible_property in enumerate(visible_properties):
            data_sync_property = next(
                (p for p in data_sync_properties if p.key == visible_property), None
            )
            if not data_sync_property:
                raise PropertyNotFound(
                    f"The property {visible_property} is not found in "
                    f"{data_sync_type.type}."
                )

            baserow_field = data_sync_property.to_baserow_field()
            baserow_field.order = index
            baserow_field.table = table
            if data_sync_property.unique_primary and not has_primary:
                has_primary = True
                baserow_field.primary = True
            baserow_field.save()

            properties_to_create.append(
                DataSyncProperty(
                    data_sync=data_sync_instance,
                    field=baserow_field,
                    key=visible_property,
                )
            )

        if not has_primary:
            raise UniquePrimaryPropertyNotFound(
                "The data sync `data_sync_type.type` didn't return a unique_primary "
                "property."
            )

        DataSyncProperty.objects.bulk_create(properties_to_create)

        # Create the table schema in the database.
        with safe_django_schema_editor() as schema_editor:
            # Django only creates indexes when the model is managed.
            model = table.get_model(managed=True)
            schema_editor.create_model(model)

        table_created.send(self, table=table, user=user)

        return data_sync_instance

    def sync_data_sync_table(self, user: AbstractUser, data_sync: DataSync):
        """
        Synchronizes the table with the data source. This will automatically create
        missing rows, update existing rows, and delete rows that no longer exist. There
        can only be one data sync active at the same time to avoid conflicts.

        :param user: The user on whose behalf the data sync is triggered.
        :param data_sync: The data sync object that must be synced.
        :return:
        """

        CoreHandler().check_permissions(
            user,
            SyncTableOperationType.type,
            workspace=data_sync.table.database.workspace,
            context=data_sync.table,
        )

        model = data_sync.table.get_model()

        data_sync_type = data_sync_type_registry.get_by_model(data_sync)
        all_properties = data_sync_type.get_properties(data_sync)
        unique_primary_keys = [p.key for p in all_properties if p.unique_primary]
        enabled_properties = DataSyncProperty.objects.filter(data_sync=data_sync)
        key_to_field_id = {p.key: f"field_{p.field_id}" for p in enabled_properties}

        existing_rows_queryset = model.objects.all().values(
            *["id"] + list(key_to_field_id.values())
        )
        existing_rows_in_table = {
            tuple(row[key_to_field_id[key]] for key in unique_primary_keys): row
            for row in existing_rows_queryset
        }
        rows_of_data_sync = {
            tuple(row[key] for key in unique_primary_keys): row
            for row in data_sync_type.get_all_rows(data_sync)
        }

        rows_to_create = []
        for new_id, data in rows_of_data_sync.items():
            if new_id not in existing_rows_in_table:
                rows_to_create.append(
                    {
                        f"field_{property.field_id}": data[property.key]
                        for property in enabled_properties
                    }
                )

        rows_to_update = []
        for existing_id, existing_record in existing_rows_in_table.items():
            if existing_id in rows_of_data_sync:
                new_record_data = rows_of_data_sync[existing_id]
                changed = False
                for field, value in new_record_data.items():
                    if existing_record[key_to_field_id[field]] != value:
                        existing_record[key_to_field_id[field]] = value
                        changed = True
                if changed:
                    rows_to_update.append(existing_record)

        row_ids_to_delete = []
        for existing_id in existing_rows_in_table.keys():
            if existing_id not in rows_of_data_sync:
                row_ids_to_delete.append(existing_rows_in_table[existing_id]["id"])

        if len(rows_to_create) > 0:
            RowHandler().create_rows(
                user=user,
                table=data_sync.table,
                model=model,
                rows_values=rows_to_create,
                generate_error_report=False,
                send_realtime_update=False,
                send_webhook_events=False,
                skip_search_update=True,
            )

        if len(rows_to_update) > 0:
            RowHandler().update_rows(
                user=user,
                table=data_sync.table,
                rows_values=rows_to_update,
                model=model,
                send_realtime_update=False,
                send_webhook_events=False,
                skip_search_update=True,
            )

        if len(row_ids_to_delete) > 0:
            RowHandler().delete_rows(
                user=user,
                table=data_sync.table,
                row_ids=row_ids_to_delete,
                model=model,
                send_realtime_update=False,
                send_webhook_events=False,
            )

        if (
            len(rows_to_create) > 0
            or len(rows_to_update) > 0
            or len(row_ids_to_delete) > 0
        ):
            SearchHandler.field_value_updated_or_created(data_sync.table)

        table_updated.send(
            self, table=data_sync.table, user=user, force_table_refresh=True
        )

    def unsync_field(self, user: AbstractUser, data_sync: DataSync, field):
        """
        Stops the sync of a field in a table, but keeps the field and the data. It
        will be converted to a normal field that can be modified, but won't be in sync
        anymore.

        :param user:
        :param data_sync:
        :param field:
        """

    def set_data_sync_visible_properties(
        self,
        user: AbstractUser,
        data_sync,
        visible_properties: List[str],
    ):
        """
        Changes the properties that are visible in the synced table. If a visible
        property is removed from the list, then it will be removed from the table, it
        won't persist like with the `unsync_field` method. If a new property is added,
        the field will be created.

        :param user:
        :param data_sync:
        :param visible_properties:
        """
