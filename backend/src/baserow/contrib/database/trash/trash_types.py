from typing import Optional, Any, List

from django.conf import settings
from django.db import connections

from baserow.contrib.database.fields.models import Field, LinkRowField
from baserow.contrib.database.fields.registries import field_type_registry
from baserow.contrib.database.fields.signals import field_restored
from baserow.contrib.database.rows.signals import row_created
from baserow.contrib.database.table.models import Table, GeneratedTableModel
from baserow.contrib.database.table.signals import table_created
from baserow.core.exceptions import TrashItemDoesNotExist
from baserow.core.models import Application, TrashEntry
from baserow.core.trash.registry import TrashableItemType


class TableTrashableItemType(TrashableItemType):
    def get_parent(self, trashed_item: Any, parent_id: int) -> Optional[Any]:
        return trashed_item.database

    def get_name(self, trashed_item: Table) -> str:
        return trashed_item.name

    def trashed_item_restored(self, trashed_item: Table, trash_entry: TrashEntry):
        table_created.send(
            self,
            table=trashed_item,
            user=None,
        )

    def permanently_delete_item(self, trashed_item: Application):
        """Deletes the table schema and instance."""

        connection = connections[settings.USER_TABLE_DATABASE]
        with connection.schema_editor() as schema_editor:
            model = trashed_item.get_model()
            schema_editor.delete_model(model)

        trashed_item.delete()

    # noinspection PyMethodMayBeStatic
    def get_items_to_trash(self, trashed_item: Table) -> List[Any]:
        """
        When trashing a link row field we also want to trash the related link row field.
        """

        model = trashed_item.get_model()
        things_to_trash = [trashed_item]
        for field in model._field_objects.values():
            field = field["field"]
            if isinstance(field, LinkRowField):
                things_to_trash.append(field.link_row_related_field)
        return things_to_trash

    type = "table"
    model_class = Table


class FieldTrashableItemType(TrashableItemType):
    def get_parent(self, trashed_item: Any, parent_id: int) -> Optional[Any]:
        return trashed_item.table

    def get_name(self, trashed_item: Field) -> str:
        return trashed_item.name

    def trashed_item_restored(self, trashed_item: Field, trash_entry: TrashEntry):
        field_restored.send(
            self,
            field=trashed_item,
            user=None,
        )

    def permanently_delete_item(self, field: Application):
        """Deletes the table schema and instance."""

        field = field.specific
        field_type = field_type_registry.get_by_model(field)

        # Remove the field from the table schema.
        connection = connections[settings.USER_TABLE_DATABASE]
        with connection.schema_editor() as schema_editor:
            from_model = field.table.get_model(field_ids=[], fields=[field])
            model_field = from_model._meta.get_field(field.db_column)
            schema_editor.remove_field(from_model, model_field)

        field.delete()

        # After the field is deleted we are going to to call the after_delete method of
        # the field type because some instance cleanup might need to happen.
        field_type.after_delete(field, from_model, connection)

    # noinspection PyMethodMayBeStatic
    def get_items_to_trash(self, trashed_item: Field) -> List[Any]:
        """
        When trashing a link row field we also want to trash the related link row field.
        """
        if isinstance(trashed_item.specific, LinkRowField):
            return [trashed_item, trashed_item.specific.link_row_related_field]
        return [trashed_item]

    type = "field"
    model_class = Field


class RowTrashableItemType(TrashableItemType):
    @property
    def requires_parent_id(self) -> bool:
        # A row is not unique just with its ID. We also need the table id (parent id)
        # to uniquely identify and lookup a specific row.
        return True

    def get_parent(self, trashed_item: Any, parent_id: int) -> Optional[Any]:
        return self._get_table(parent_id)

    @staticmethod
    def _get_table(parent_id):
        try:
            return Table.objects_and_trash.get(id=parent_id)
        except Table.DoesNotExist:
            # The parent table must have been actually deleted, in which case the
            # row itself no longer exits.
            raise TrashItemDoesNotExist()

    def get_name(self, trashed_item) -> str:
        return str(trashed_item.id)

    def trashed_item_restored(self, trashed_item, trash_entry: TrashEntry):
        table = self.get_parent(trashed_item, trash_entry.parent_trash_item_id)

        model = table.get_model()
        row_created.send(
            self,
            row=trashed_item,
            table=table,
            model=model,
            before=None,
            user=None,
        )

    def permanently_delete_item(self, row):
        row.delete()

    def lookup_trashed_item(
        self, trashed_entry: TrashEntry, trash_item_lookup_cache=None
    ):
        """
        Returns the actual instance of the trashed item. By default simply does a get
        on the model_class's trash manager.

        :param trash_item_lookup_cache: A cache dict used to store the generated models
            for a given table so if looking up many rows from the same table we only
            need to lookup the tables fields etc once.
        :param trashed_entry: The entry to get the real trashed instance for.
        :return: An instance of the model_class with trashed_item_id
        """

        # Cache the expensive table.get_model function call if we are looking up
        # many trash items at once.
        if trash_item_lookup_cache is not None:
            model_cache = trash_item_lookup_cache.setdefault(
                "row_table_model_cache", {}
            )
            try:
                model = model_cache[trashed_entry.parent_trash_item_id]
            except KeyError:
                model = model_cache.setdefault(
                    trashed_entry.parent_trash_item_id,
                    self._get_table_model(trashed_entry.parent_trash_item_id),
                )
        else:
            model = self._get_table_model(trashed_entry.parent_trash_item_id)

        try:
            return model.trash.get(id=trashed_entry.trash_item_id)
        except model.DoesNotExist:
            raise TrashItemDoesNotExist()

    def _get_table_model(self, table_id):
        table = self._get_table(table_id)
        return table.get_model()

    # noinspection PyMethodMayBeStatic
    def get_extra_description(self, trashed_item: Any, table) -> Optional[str]:

        model = table.get_model()
        for field in model._field_objects.values():
            if field["field"].primary:
                primary_value = field["type"].get_human_readable_value(
                    getattr(trashed_item, field["name"]), field
                )
                if primary_value is None or primary_value == "":
                    primary_value = f"unnamed row {trashed_item.id}"
                return primary_value

        return "unknown row"

    type = "row"
    model_class = GeneratedTableModel
