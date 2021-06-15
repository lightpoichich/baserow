import pytest
from django.db import connection

from baserow.contrib.database.fields.handler import FieldHandler
from baserow.contrib.database.fields.models import Field, TextField, LinkRowField
from baserow.contrib.database.rows.handler import RowHandler
from baserow.contrib.database.table.models import Table
from baserow.core.trash.handler import TrashHandler


@pytest.mark.django_db
def test_delete_row(data_fixture):
    user = data_fixture.create_user()
    table = data_fixture.create_database_table(name="Car", user=user)
    data_fixture.create_text_field(table=table, name="Name", text_default="Test")

    handler = RowHandler()
    model = table.get_model()
    row = handler.create_row(user=user, table=table)
    handler.create_row(user=user, table=table)

    TrashHandler.permanently_delete(row)
    assert model.objects.all().count() == 1


@pytest.mark.django_db
def test_perm_delete_table(data_fixture):
    user = data_fixture.create_user()
    group = data_fixture.create_group(user=user)
    database = data_fixture.create_database_application(group=group)
    table = data_fixture.create_database_table(user=user, database=database)

    assert Table.objects.all().count() == 1
    assert f"database_table_{table.id}" in connection.introspection.table_names()

    TrashHandler.permanently_delete(table)

    assert Table.objects.all().count() == 0
    assert f"database_table_{table.id}" not in connection.introspection.table_names()


@pytest.mark.django_db
def test_perm_delete_field(data_fixture):
    user = data_fixture.create_user()
    table = data_fixture.create_database_table(user=user)
    text_field = data_fixture.create_text_field(table=table)

    assert Field.objects.all().count() == 1
    assert TextField.objects.all().count() == 1
    TrashHandler.permanently_delete(text_field)
    assert Field.objects.all().count() == 0
    assert Field.trash.all().count() == 0
    assert TextField.objects.all().count() == 0

    table_model = table.get_model()
    field_name = f"field_{text_field.id}"
    assert field_name not in [field.name for field in table_model._meta.get_fields()]
    assert f"trashed_{field_name}" not in [
        field.name for field in table_model._meta.get_fields()
    ]


@pytest.mark.django_db
def test_perm_delete_link_row_field(data_fixture):
    user = data_fixture.create_user()
    database = data_fixture.create_database_application(user=user, name="Placeholder")
    table = data_fixture.create_database_table(name="Example", database=database)
    customers_table = data_fixture.create_database_table(
        name="Customers", database=database
    )
    cars_table = data_fixture.create_database_table(name="Cars", database=database)
    data_fixture.create_database_table(name="Unrelated")

    field_handler = FieldHandler()
    row_handler = RowHandler()

    # Create a primary field and some example data for the customers table.
    customers_primary_field = field_handler.create_field(
        user=user, table=customers_table, type_name="text", name="Name", primary=True
    )
    row_handler.create_row(
        user=user,
        table=customers_table,
        values={f"field_{customers_primary_field.id}": "John"},
    )
    row_handler.create_row(
        user=user,
        table=customers_table,
        values={f"field_{customers_primary_field.id}": "Jane"},
    )

    # Create a primary field and some example data for the cars table.
    cars_primary_field = field_handler.create_field(
        user=user, table=cars_table, type_name="text", name="Name", primary=True
    )
    row_handler.create_row(
        user=user, table=cars_table, values={f"field_{cars_primary_field.id}": "BMW"}
    )
    row_handler.create_row(
        user=user, table=cars_table, values={f"field_{cars_primary_field.id}": "Audi"}
    )

    link_field_1 = field_handler.create_field(
        user=user,
        table=table,
        type_name="link_row",
        name="Customer",
        link_row_table=customers_table,
    )
    TrashHandler.permanently_delete(link_field_1)
    assert LinkRowField.objects.all().count() == 0
    for t in connection.introspection.table_names():
        if "_relation_" in t:
            assert False


@pytest.mark.django_db
def test_trashing_a_table_with_link_fields_pointing_at_it_also_trashes_those_fields(
    data_fixture,
):
    user = data_fixture.create_user()
    database = data_fixture.create_database_application(user=user, name="Placeholder")
    table = data_fixture.create_database_table(name="Example", database=database)
    customers_table = data_fixture.create_database_table(
        name="Customers", database=database
    )
    cars_table = data_fixture.create_database_table(name="Cars", database=database)

    field_handler = FieldHandler()
    row_handler = RowHandler()

    # Create a primary field and some example data for the customers table.
    customers_primary_field = field_handler.create_field(
        user=user, table=customers_table, type_name="text", name="Name", primary=True
    )
    row_handler.create_row(
        user=user,
        table=customers_table,
        values={f"field_{customers_primary_field.id}": "John"},
    )
    row_handler.create_row(
        user=user,
        table=customers_table,
        values={f"field_{customers_primary_field.id}": "Jane"},
    )

    # Create a primary field and some example data for the cars table.
    cars_primary_field = field_handler.create_field(
        user=user, table=cars_table, type_name="text", name="Name", primary=True
    )
    row_handler.create_row(
        user=user, table=cars_table, values={f"field_{cars_primary_field.id}": "BMW"}
    )
    row_handler.create_row(
        user=user, table=cars_table, values={f"field_{cars_primary_field.id}": "Audi"}
    )

    link_field_1 = field_handler.create_field(
        user=user,
        table=table,
        type_name="link_row",
        name="Customer",
        link_row_table=customers_table,
    )
    TrashHandler.trash(user, database.group, database, customers_table)

    link_field_1.refresh_from_db()
    assert link_field_1.trashed


@pytest.mark.django_db
def test_trashed_row_entry_includes_the_rows_primary_key_value_as_an_extra_description(
    data_fixture,
):
    user = data_fixture.create_user()
    database = data_fixture.create_database_application(user=user, name="Placeholder")
    customers_table = data_fixture.create_database_table(
        name="Customers", database=database
    )

    field_handler = FieldHandler()
    row_handler = RowHandler()

    # Create a primary field and some example data for the customers table.
    customers_primary_field = field_handler.create_field(
        user=user, table=customers_table, type_name="text", name="Name", primary=True
    )
    row = row_handler.create_row(
        user=user,
        table=customers_table,
        values={f"field_{customers_primary_field.id}": "John"},
    )
    trash_entry = TrashHandler.trash(
        user, database.group, database, row, parent_id=customers_table.id
    )

    assert trash_entry.extra_description == "John"
    assert trash_entry.name == "Row " + str(row.id)
    assert trash_entry.parent_name == "Customers"


@pytest.mark.django_db
def test_trashed_row_entry_extra_description_is_unnamed_when_no_value_pk(
    data_fixture,
):
    user = data_fixture.create_user()
    database = data_fixture.create_database_application(user=user, name="Placeholder")
    customers_table = data_fixture.create_database_table(
        name="Customers", database=database
    )

    field_handler = FieldHandler()
    row_handler = RowHandler()

    # Create a primary field and some example data for the customers table.
    field_handler.create_field(
        user=user, table=customers_table, type_name="text", name="Name", primary=True
    )
    row = row_handler.create_row(
        user=user,
        table=customers_table,
        values={},
    )
    trash_entry = TrashHandler.trash(
        user, database.group, database, row, parent_id=customers_table.id
    )

    assert trash_entry.extra_description == f"unnamed row {row.id}"
    assert trash_entry.name == "Row " + str(row.id)
    assert trash_entry.parent_name == "Customers"


@pytest.mark.django_db
def test_restoring_a_trashed_link_field_restores_the_opposing_field_also(
    data_fixture,
):
    user = data_fixture.create_user()
    database = data_fixture.create_database_application(user=user, name="Placeholder")
    table = data_fixture.create_database_table(database=database)
    customers_table = data_fixture.create_database_table(
        name="Customers", database=database
    )

    field_handler = FieldHandler()
    row_handler = RowHandler()

    # Create a primary field and some example data for the customers table.
    customers_primary_field = field_handler.create_field(
        user=user, table=customers_table, type_name="text", name="Name", primary=True
    )
    row_handler.create_row(
        user=user,
        table=customers_table,
        values={f"field_{customers_primary_field.id}": "John"},
    )
    row_handler.create_row(
        user=user,
        table=customers_table,
        values={f"field_{customers_primary_field.id}": "Jane"},
    )

    link_field_1 = field_handler.create_field(
        user=user,
        table=table,
        type_name="link_row",
        name="Customer",
        link_row_table=customers_table,
    )
    TrashHandler.trash(user, database.group, database, link_field_1)

    assert LinkRowField.trash.count() == 2

    TrashHandler.restore_item(user, "field", table.id, link_field_1.id)

    assert LinkRowField.objects.count() == 2


@pytest.mark.django_db
def test_trashing_a_row_hides_it_from_a_link_row_field_pointing_at_it(
    data_fixture,
):
    user = data_fixture.create_user()
    database = data_fixture.create_database_application(user=user, name="Placeholder")
    customers_table = data_fixture.create_database_table(
        name="Customers", database=database
    )
    cars_table = data_fixture.create_database_table(name="Cars", database=database)

    field_handler = FieldHandler()
    row_handler = RowHandler()

    # Create a primary field and some example data for the customers table.
    customers_primary_field = field_handler.create_field(
        user=user, table=customers_table, type_name="text", name="Name", primary=True
    )
    john_row = row_handler.create_row(
        user=user,
        table=customers_table,
        values={f"field_{customers_primary_field.id}": "John"},
    )
    jane_row = row_handler.create_row(
        user=user,
        table=customers_table,
        values={f"field_{customers_primary_field.id}": "Jane"},
    )

    link_field_1 = field_handler.create_field(
        user=user,
        table=cars_table,
        type_name="link_row",
        name="customer",
        link_row_table=customers_table,
    )
    # Create a primary field and some example data for the cars table.
    cars_primary_field = field_handler.create_field(
        user=user, table=cars_table, type_name="text", name="Name", primary=True
    )
    linked_row_pointing_at_john = row_handler.create_row(
        user=user,
        table=cars_table,
        values={
            f"field_{cars_primary_field.id}": "BMW",
            f"field_{link_field_1.id}": [john_row.id],
        },
    )
    linked_row_pointing_at_jane = row_handler.create_row(
        user=user,
        table=cars_table,
        values={
            f"field_{cars_primary_field.id}": "Audi",
            f"field_{link_field_1.id}": [jane_row.id],
        },
    )

    cars_model = cars_table.get_model(attribute_names=True)
    assert list(cars_model.objects.values_list("customer", flat=True)) == [
        john_row.id,
        jane_row.id,
    ]
    row = RowHandler().get_row(user, cars_table, linked_row_pointing_at_john.id)
    assert list(
        getattr(row, f"field_{link_field_1.id}").values_list("id", flat=True)
    ) == [john_row.id]

    TrashHandler.trash(
        user, database.group, database, john_row, parent_id=customers_table.id
    )

    row = RowHandler().get_row(user, cars_table, linked_row_pointing_at_john.id)
    assert list(getattr(row, f"field_{link_field_1.id}").all()) == []
    row = RowHandler().get_row(user, cars_table, linked_row_pointing_at_jane.id)
    assert list(
        getattr(row, f"field_{link_field_1.id}").values_list("id", flat=True)
    ) == [jane_row.id]
