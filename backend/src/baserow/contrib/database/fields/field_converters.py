from .registries import FieldConverter
from .models import CreatedOnField, LastModifiedField, LinkRowField, FileField
from django.db import models
from django.db.models.expressions import RawSQL


class RecreateFieldConverter(FieldConverter):
    def alter_field(
        self,
        from_field,
        to_field,
        from_model,
        to_model,
        from_model_field,
        to_model_field,
        user,
        connection,
    ):
        """
        Does the field alteration by removing the old field and creating the new field.
        The success rate of this converter is very high, but the downside is that the
        data is lost.
        """

        with connection.schema_editor() as schema_editor:
            schema_editor.remove_field(from_model, from_model_field)
            schema_editor.add_field(to_model, to_model_field)


class LinkRowFieldConverter(RecreateFieldConverter):
    type = "link_row"

    def is_applicable(self, from_model, from_field, to_field):
        return (
            (
                isinstance(from_field, LinkRowField)
                and not isinstance(to_field, LinkRowField)
            )
            or (
                not isinstance(from_field, LinkRowField)
                and isinstance(to_field, LinkRowField)
            )
            or (
                # If both fields are LinkRowFields and neither the linked table nor the
                # multiple setting has changed.
                isinstance(from_field, LinkRowField)
                and isinstance(to_field, LinkRowField)
                and from_field.link_row_table_id != to_field.link_row_table_id
            )
        )


class FileFieldConverter(RecreateFieldConverter):
    type = "file"

    def is_applicable(self, from_model, from_field, to_field):
        return (
            isinstance(from_field, FileField) and not isinstance(to_field, FileField)
        ) or (not isinstance(from_field, FileField) and isinstance(to_field, FileField))


class CreatedOnLastModifiedBaseConverter(RecreateFieldConverter):
    def alter_field(
        self,
        from_field,
        to_field,
        from_model,
        to_model,
        from_model_field,
        to_model_field,
        user,
        connection,
    ):
        """
        Base class for converting to the correct update_on/created_on
        Values, when changing from datetime to date or vice versa.
        """

        if self.type == "last_modified":
            db_column_to_use = "updated_on"
        else:
            db_column_to_use = "created_on"

        is_from_datetime_to_date = (
            from_field.date_include_time and not to_field.date_include_time
        )
        is_from_date_to_datetime = (
            not from_field.date_include_time and to_field.date_include_time
        )
        with connection.schema_editor() as schema_editor:
            schema_editor.remove_field(from_model, from_model_field)
            schema_editor.add_field(to_model, to_model_field)

        if is_from_date_to_datetime:
            to_model.objects.all().update(
                **{f"{to_field.db_column}": models.F(db_column_to_use)}
            )
            return

        if is_from_datetime_to_date:
            annotation_sql = f"{db_column_to_use} at time zone '{to_field.timezone}'"
            sql = RawSQL(
                annotation_sql,
                params=[],
                output_field=to_model_field,
            )
            to_model.objects.all().annotate(val=sql).update(
                **{f"{to_field.db_column}": models.F("val")}
            )


class LastModifiedFieldConverter(CreatedOnLastModifiedBaseConverter):
    type = "last_modified"

    def is_applicable(self, from_model, from_field, to_field):
        """
        The Field Converter for the LastModifiedField should only run if there is a
        conversion from LastModifiedField without timestamp to LastModifiedField
        with timestamp or vice versa.
        """

        if not isinstance(from_field, LastModifiedField) or not isinstance(
            to_field, LastModifiedField
        ):
            return False

        return (
            not from_field.date_include_time
            and to_field.date_include_time
            or from_field.date_include_time
            and not to_field.date_include_time
        )


class CreatedOnFieldConverter(CreatedOnLastModifiedBaseConverter):
    type = "created_on"

    def is_applicable(self, from_model, from_field, to_field):
        """
        The Field Converter for the CreatedOnField should only run if there is a
        conversion from CreatedOnField without timestamp to CreatedOnField
        with timestamp or vice versa.
        """

        if not isinstance(from_field, CreatedOnField) or not isinstance(
            to_field, CreatedOnField
        ):
            return False

        return (not from_field.date_include_time and to_field.date_include_time) or (
            from_field.date_include_time and not to_field.date_include_time
        )
