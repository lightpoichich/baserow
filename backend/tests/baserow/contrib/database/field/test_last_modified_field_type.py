import pytest
from baserow.contrib.database.fields.models import LastModifiedField
from baserow.contrib.database.fields.handler import FieldHandler
from baserow.contrib.database.rows.handler import RowHandler


@pytest.mark.django_db
def test_last_modified_field_type(data_fixture):
    user = data_fixture.create_user()
    table = data_fixture.create_database_table(user=user)

    field_handler = FieldHandler()
    row_handler = RowHandler()

    last_modified_field_date = field_handler.create_field(
        user=user, table=table, type_name="last_modified", name="Last Date"
    )
    last_modified_field_datetime = field_handler.create_field(
        user=user,
        table=table,
        type_name="last_modified",
        name="Last Datetime",
        date_include_time=True,
    )
    assert last_modified_field_date.date_include_time is False
    assert last_modified_field_datetime.date_include_time is True
    assert len(LastModifiedField.objects.all()) == 2

    model = table.get_model(attribute_names=True)

    row = row_handler.create_row(user=user, table=table, values={}, model=model)
    assert row.last_date is not None
    assert row.last_date == row.updated_on.date()

    assert row.last_date is not None
    row_last_modified_2 = row.last_datetime.replace(microsecond=0)
    row_updated_on = row.updated_on.replace(microsecond=0)
    assert row_last_modified_2 == row_updated_on

    # trying to set the fields at a specific date/datetime will still update
    # the values with the updated_on timestamp
    row = row_handler.create_row(
        user=user,
        table=table,
        values={
            "last_date": "2020-4-1",
            "last_datetime": "2020-4-1 12:30:30",
        },
        model=model,
    )
    row.refresh_from_db()
    assert row.last_date == row.updated_on.date()

    row_updated_on = row.updated_on.replace(microsecond=0)
    row_last_modified_2 = row.last_datetime.replace(microsecond=0)
    assert row_last_modified_2 == row_updated_on

    row_last_modified_2_before_alter = row.last_datetime

    # changing the field from LastModified to Datetime should persist the date
    # without microseconds and seconds
    field_handler.update_field(
        user=user,
        field=last_modified_field_datetime,
        new_type_name="date",
        date_include_time=True,
    )

    assert len(LastModifiedField.objects.all()) == 1
    row.refresh_from_db()
    assert row.last_datetime == row_last_modified_2_before_alter.replace(
        microsecond=0, second=0
    )

    # changing the field from LastModified with Datetime to Text Field should persist the datetime as string
    field_handler.update_field(
        user=user,
        field=last_modified_field_datetime,
        new_type_name="last_modified",
        date_include_time=True,
    )
    assert len(LastModifiedField.objects.all()) == 2

    row.refresh_from_db()
    row_last_modified_2_before_alter = row.last_datetime
    field_handler.update_field(
        user=user,
        field=last_modified_field_datetime,
        new_type_name="text",
    )
    row.refresh_from_db()
    assert len(LastModifiedField.objects.all()) == 1
    assert row.last_datetime == row_last_modified_2_before_alter.strftime(
        "%d/%m/%Y %H:%M"
    )

    # deleting the fields
    field_handler.delete_field(user=user, field=last_modified_field_date)

    assert len(LastModifiedField.objects.all()) == 0
