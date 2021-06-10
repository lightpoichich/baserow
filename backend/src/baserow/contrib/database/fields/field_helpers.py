from decimal import Decimal
from typing import Dict, Any, List

from django.utils.dateparse import parse_datetime, parse_date
from django.utils.timezone import make_aware, utc

from baserow.contrib.database.fields.handler import FieldHandler
from baserow.contrib.database.fields.models import SelectOption
from baserow.contrib.database.fields.registries import field_type_registry
from baserow.contrib.database.rows.handler import RowHandler


def _parse_datetime(datetime):
    return make_aware(parse_datetime(datetime), timezone=utc)


def _parse_date(date):
    return parse_date(date)


def construct_all_possible_field_kwargs(
    link_table, decimal_link_table, file_link_table
) -> Dict[str, List[Dict[str, Any]]]:
    """
    Some baserow field types have multiple different 'modes' which result in
    different different database columns and modes of operation being
    created. This function creates a dictionary of field type to a list of
    kwarg dicts, one for each interesting possible 'subtype' of the field.
    """
    all_interesting_field_kwargs = {
        "text": [{"name": "text"}],
        "long_text": [{"name": "long_text"}],
        "url": [{"name": "url"}],
        "email": [{"name": "email"}],
        "number": [
            {"name": "negative_int", "number_type": "INTEGER", "number_negative": True},
            {
                "name": "positive_int",
                "number_type": "INTEGER",
                "number_negative": False,
            },
            {
                "name": "negative_decimal",
                "number_type": "DECIMAL",
                "number_negative": "True",
            },
            {
                "name": "positive_decimal",
                "number_type": "DECIMAL",
                "number_negative": False,
            },
        ],
        "boolean": [{"name": "boolean"}],
        "date": [
            {"name": "datetime_us", "date_include_time": True, "date_format": "US"},
            {"name": "date_us", "date_include_time": False, "date_format": "US"},
            {"name": "datetime_eu", "date_include_time": True, "date_format": "EU"},
            {"name": "date_eu", "date_include_time": False, "date_format": "EU"},
        ],
        "link_row": [
            {"name": "link_row", "link_row_table": link_table},
            {"name": "decimal_link_row", "link_row_table": decimal_link_table},
            {"name": "file_link_row", "link_row_table": file_link_table},
        ],
        "file": [{"name": "file"}],
        "single_select": [
            {
                "name": "single_select",
                "select_options": [
                    {"id": 0, "value": "A", "color": "red"},
                    {"id": 1, "value": "B", "color": "blue"},
                ],
            }
        ],
        "phone_number": [{"name": "phone_number"}],
    }
    # If you have added a new field please add an entry into the dict above with any
    # test worthy combinations of kwargs
    assert set(field_type_registry.get_types()) == set(
        all_interesting_field_kwargs.keys()
    ), "Please add the new field type to the testing dictionary of interesting kwargs"
    return all_interesting_field_kwargs


def setup_interesting_test_table(data_fixture):
    """
    Constructs a testing table with every field type, their sub types and any other
    interesting baserow edge cases worth testing when writing a comphensive "does this
    feature work with all the baserow fields" test.

    :param data_fixture: The baserow testing data_fixture object
    :return:
    """

    user = data_fixture.create_user()
    database = data_fixture.create_database_application(user=user)
    table = data_fixture.create_database_table(database=database, user=user)
    link_table = data_fixture.create_database_table(database=database, user=user)
    decimal_link_table = data_fixture.create_database_table(
        database=database, user=user
    )
    file_link_table = data_fixture.create_database_table(database=database, user=user)
    handler = FieldHandler()
    all_possible_kwargs_per_type = construct_all_possible_field_kwargs(
        link_table, decimal_link_table, file_link_table
    )
    name_to_field_id = {}
    i = 0
    for field_type_name, all_possible_kwargs in all_possible_kwargs_per_type.items():
        for kwargs in all_possible_kwargs:
            field = handler.create_field(
                user=user,
                table=table,
                type_name=field_type_name,
                order=i,
                **kwargs,
            )
            i += 1
            name_to_field_id[kwargs["name"]] = field.id
    row_handler = RowHandler()
    other_table_primary_text_field = data_fixture.create_text_field(
        table=link_table, name="text_field", primary=True
    )
    other_table_primary_decimal_field = data_fixture.create_number_field(
        table=decimal_link_table,
        name="text_field",
        primary=True,
        number_type="DECIMAL",
        number_decimal_places=3,
        number_negative=True,
    )
    other_table_primary_file_field = data_fixture.create_file_field(
        table=file_link_table,
        name="file_field",
        primary=True,
    )

    model = table.get_model()
    datetime = _parse_datetime("2020-02-01 01:23")
    date = _parse_date("2020-02-01")

    values = {
        "text": "text",
        "long_text": "long_text",
        "url": "https://www.google.com",
        "email": "test@example.com",
        "negative_int": -1,
        "positive_int": 1,
        "negative_decimal": Decimal("-1.2"),
        "positive_decimal": Decimal("1.2"),
        "boolean": "True",
        "datetime_us": datetime,
        "date_us": date,
        "datetime_eu": datetime,
        "date_eu": date,
        # We will setup link rows manually later
        "link_row": None,
        "decimal_link_row": None,
        "file_link_row": None,
        "file": [
            {"name": "hashed_name.txt", "visible_name": "a.txt"},
            {"name": "other_name.txt", "visible_name": "b.txt"},
        ],
        "single_select": SelectOption.objects.get(value="A"),
        "phone_number": "+4412345678",
    }

    missing_fields = set(name_to_field_id.keys()) - set(values.keys())
    assert values.keys() == name_to_field_id.keys(), (
        "Please update the dictionary above with interesting test values for your new "
        f"field type. In the values dict you are missing the fields {missing_fields}."
    )
    row_values = {}
    for field_type, val in values.items():
        if val is not None:
            row_values[f"field_{name_to_field_id[field_type]}"] = val
    # Make a blank row to test empty field conversion also.
    model.objects.create(**{})
    row = model.objects.create(**row_values)

    # Setup the link rows
    linked_row_1 = row_handler.create_row(
        user=user,
        table=link_table,
        values={
            other_table_primary_text_field.id: "linked_row_1",
        },
    )
    linked_row_2 = row_handler.create_row(
        user=user,
        table=link_table,
        values={
            other_table_primary_text_field.id: "linked_row_2",
        },
    )
    linked_row_3 = row_handler.create_row(
        user=user,
        table=link_table,
        values={
            other_table_primary_text_field.id: None,
        },
    )
    linked_row_4 = row_handler.create_row(
        user=user,
        table=decimal_link_table,
        values={
            other_table_primary_decimal_field.id: "1.234",
        },
    )
    linked_row_5 = row_handler.create_row(
        user=user,
        table=decimal_link_table,
        values={
            other_table_primary_decimal_field.id: "-123.456",
        },
    )
    linked_row_6 = row_handler.create_row(
        user=user,
        table=decimal_link_table,
        values={
            other_table_primary_decimal_field.id: None,
        },
    )
    user_file_1 = data_fixture.create_user_file(
        original_name="name.txt", unique="test", sha256_hash="hash"
    )
    linked_row_7 = row_handler.create_row(
        user=user,
        table=file_link_table,
        values={
            other_table_primary_file_field.id: [{"name": user_file_1.name}],
        },
    )
    linked_row_8 = row_handler.create_row(
        user=user,
        table=file_link_table,
        values={
            other_table_primary_file_field.id: None,
        },
    )

    getattr(row, f"field_{name_to_field_id['link_row']}").add(
        linked_row_1.id, linked_row_2.id, linked_row_3.id
    )
    getattr(row, f"field_{name_to_field_id['decimal_link_row']}").add(
        linked_row_4.id, linked_row_5.id, linked_row_6.id
    )
    getattr(row, f"field_{name_to_field_id['file_link_row']}").add(
        linked_row_7.id, linked_row_8.id
    )
    return table, user
