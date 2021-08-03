import pytest
from baserow.contrib.database.fields.models import CreatedOnField
from baserow.contrib.database.fields.handler import FieldHandler
from baserow.contrib.database.rows.handler import RowHandler


@pytest.mark.django_db
def test_created_on_field_type(data_fixture):
    user = data_fixture.create_user()
    table = data_fixture.create_database_table(user=user)

    field_handler = FieldHandler()
    row_handler = RowHandler()

    created_on_field_date = field_handler.create_field(
        user=user,
        table=table,
        type_name="created_on",
        name="Create Date",
        timezone="Europe/Berlin",
    )
    created_on_field_datetime = field_handler.create_field(
        user=user,
        table=table,
        type_name="created_on",
        name="Create Datetime",
        date_include_time=True,
        timezone="Europe/Berlin",
    )
    assert created_on_field_date.date_include_time is False
    assert created_on_field_datetime.date_include_time is True
    assert len(CreatedOnField.objects.all()) == 2

    model = table.get_model(attribute_names=True)

    row = row_handler.create_row(user=user, table=table, values={}, model=model)
    assert row.create_date is not None
    assert row.create_date == row.created_on.date()

    assert row.create_date is not None
    row_create_datetime = row.create_datetime.replace(microsecond=0)
    row_created_on = row.created_on.replace(microsecond=0)
    assert row_create_datetime == row_created_on

    # trying to set the fields at a specific date/datetime will still update
    # the values with the updated_on timestamp
    row = row_handler.create_row(
        user=user,
        table=table,
        values={
            "create_date": "2020-4-1",
            "create_datetime": "2020-4-1 12:30:30",
        },
        model=model,
    )
    row.refresh_from_db()
    assert row.create_date == row.created_on.date()

    assert row.created_on.replace(microsecond=0) == row.create_datetime.replace(
        microsecond=0
    )

    row_create_datetime_before_alter = row.create_datetime

    # changing the field from LastModified to Datetime should persist the date
    # without microseconds and seconds
    field_handler.update_field(
        user=user,
        field=created_on_field_datetime,
        new_type_name="date",
        date_include_time=True,
    )

    assert len(CreatedOnField.objects.all()) == 1
    row.refresh_from_db()
    assert row.create_datetime == row_create_datetime_before_alter.replace(
        microsecond=0, second=0
    )

    # changing the field from LastModified with Datetime to Text Field should persist
    # the datetime as string
    field_handler.update_field(
        user=user,
        field=created_on_field_datetime,
        new_type_name="created_on",
        date_include_time=True,
        timezone="Europe/Berlin",
    )
    assert len(CreatedOnField.objects.all()) == 2

    row.refresh_from_db()
    row_create_datetime_before_alter = row.create_datetime
    field_handler.update_field(
        user=user,
        field=created_on_field_datetime,
        new_type_name="text",
    )
    row.refresh_from_db()
    assert len(CreatedOnField.objects.all()) == 1
    assert row.create_datetime == row_create_datetime_before_alter.strftime(
        "%d/%m/%Y %H:%M"
    )

    # deleting the fields
    field_handler.delete_field(user=user, field=created_on_field_date)

    assert len(CreatedOnField.objects.all()) == 0


@pytest.mark.django_db
def test_last_modified_field_type_wrong_timezone(data_fixture):
    user = data_fixture.create_user()
    table = data_fixture.create_database_table(user=user)

    field_handler = FieldHandler()

    with pytest.raises(ValueError):
        field_handler.create_field(
            user=user,
            table=table,
            type_name="created_on",
            name="Create Date",
            timezone="SDj",
        )
