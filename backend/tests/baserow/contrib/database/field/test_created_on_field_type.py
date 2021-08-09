import pytest
from pytz import timezone
from baserow.contrib.database.fields.models import CreatedOnField
from baserow.contrib.database.fields.handler import FieldHandler
from baserow.contrib.database.rows.handler import RowHandler


@pytest.mark.django_db
def test_created_on_field_type(data_fixture):
    user = data_fixture.create_user()
    table = data_fixture.create_database_table(user=user)

    field_handler = FieldHandler()
    row_handler = RowHandler()
    timezone_to_test = "Europe/Berlin"
    timezone_of_field = timezone(timezone_to_test)

    data_fixture.create_text_field(table=table, name="text_field", primary=True)
    created_on_field_date = field_handler.create_field(
        user=user,
        table=table,
        type_name="created_on",
        name="Create Date",
        timezone=timezone_to_test,
    )
    created_on_field_datetime = field_handler.create_field(
        user=user,
        table=table,
        type_name="created_on",
        name="Create Datetime",
        date_include_time=True,
        timezone=timezone_to_test,
    )
    assert created_on_field_date.date_include_time is False
    assert created_on_field_datetime.date_include_time is True
    assert len(CreatedOnField.objects.all()) == 2

    model = table.get_model(attribute_names=True)

    row = row_handler.create_row(user=user, table=table, values={}, model=model)
    assert row.create_date is not None
    assert row.create_date.replace(microsecond=0) == row.created_on.replace(
        microsecond=0
    )

    assert row.create_date is not None
    row_create_datetime = row.create_datetime.replace(microsecond=0)
    row_created_on = row.created_on.replace(microsecond=0)
    assert row_create_datetime == row_created_on

    # Updating the text field will NOT updated
    # the created_on field.
    row_create_datetime_before_update = row.create_datetime
    row_create_date_before_update = row.create_date
    row_handler.update_row(
        user=user,
        table=table,
        row_id=row.id,
        values={
            "text_field": "Hello Test",
        },
        model=model,
    )

    row.refresh_from_db()
    assert row.create_datetime == row_create_datetime_before_update
    assert row.create_date == row_create_date_before_update

    row_create_datetime_before_alter = row.create_datetime

    # changing the field from CreatedOn to Datetime should persist the date
    # without microseconds and seconds in the corresponding timezone
    field_handler.update_field(
        user=user,
        field=created_on_field_datetime,
        new_type_name="date",
        date_include_time=True,
    )

    assert len(CreatedOnField.objects.all()) == 1
    row.refresh_from_db()
    field_before_with_timezone = row_create_datetime_before_alter.replace(
        microsecond=0, second=0
    ).astimezone(timezone_of_field)
    assert row.create_datetime.year == field_before_with_timezone.year
    assert row.create_datetime.month == field_before_with_timezone.month
    assert row.create_datetime.day == field_before_with_timezone.day
    assert row.create_datetime.hour == field_before_with_timezone.hour
    assert row.create_datetime.minute == field_before_with_timezone.minute
    assert row.create_datetime.second == field_before_with_timezone.second

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
    assert row.create_datetime == row_create_datetime_before_alter.astimezone(
        timezone_of_field
    ).strftime("%d/%m/%Y %H:%M")

    # deleting the fields
    field_handler.delete_field(user=user, field=created_on_field_date)

    assert len(CreatedOnField.objects.all()) == 0


@pytest.mark.django_db
def test_created_on_field_type_wrong_timezone(data_fixture):
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
