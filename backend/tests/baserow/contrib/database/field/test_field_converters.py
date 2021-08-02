import pytest

from baserow.contrib.database.fields.models import LinkRowField
from baserow.contrib.database.fields.field_converters import (
    LastModifiedFieldConverter,
    LinkRowFieldConverter,
)


@pytest.mark.django_db
def test_link_row_field_converter_applicable(data_fixture):
    table = data_fixture.create_database_table()
    table_2 = data_fixture.create_database_table(database=table.database)
    table_3 = data_fixture.create_database_table(database=table.database)
    text_field = data_fixture.create_text_field(table=table)
    link_row_field_1 = LinkRowField.objects.create(
        table=table, link_row_table=table_2, order=1
    )
    link_row_field_2 = LinkRowField.objects.create(
        table=table, link_row_table=table_3, order=2
    )
    link_row_field_3 = LinkRowField.objects.create(
        table=table, link_row_table=table_2, order=3
    )

    converter = LinkRowFieldConverter()
    assert converter.is_applicable(None, text_field, link_row_field_1)
    assert converter.is_applicable(None, link_row_field_1, text_field)
    assert converter.is_applicable(None, link_row_field_1, link_row_field_2)
    assert converter.is_applicable(None, link_row_field_2, link_row_field_1)
    assert not converter.is_applicable(None, link_row_field_1, link_row_field_3)


@pytest.mark.django_db
def test_last_modified_field_converter_applicable(data_fixture):
    table = data_fixture.create_database_table()
    text_field = data_fixture.create_text_field(table=table)
    last_modified_field_datetime = data_fixture.create_last_modified_field(
        table=table, date_include_time=True
    )
    last_modified_field_date = data_fixture.create_last_modified_field(table=table)
    converter = LastModifiedFieldConverter()
    assert not converter.is_applicable(None, text_field, last_modified_field_date)
    assert not converter.is_applicable(
        None, last_modified_field_datetime, last_modified_field_date
    )
    assert converter.is_applicable(
        None, last_modified_field_date, last_modified_field_datetime
    )
