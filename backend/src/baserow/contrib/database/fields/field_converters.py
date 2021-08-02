from .registries import FieldConverter
from .models import LastModifiedField, LinkRowField, FileField
from django.db import models


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


class LastModifiedFieldConverter(RecreateFieldConverter):
    type = "last_modified"

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
        In case there is a conversion for the LastModifiedField from
        'without timestamp' to 'with timestamp' we need to make sure
        that the field gets the timestamp or date from the 'updated_on'
        column.
        """

        with connection.schema_editor() as schema_editor:
            schema_editor.remove_field(from_model, from_model_field)
            schema_editor.add_field(to_model, to_model_field)

        to_model.objects.all().update(
            **{f"{to_field.db_column}": models.F("updated_on")}
        )

    def is_applicable(self, from_model, from_field, to_field):
        """
        The Field Converter for the LastModifiedField should only run if there is a
        conversion from LastModifiedField without timestamp to LastModifiedField
        with timestamp.
        """

        from_date_to_timestamp = (
            not from_field.date_include_time and to_field.date_include_time
        )
        return (
            isinstance(from_field, LastModifiedField)
            and isinstance(to_field, LastModifiedField)
            and from_date_to_timestamp
        )
