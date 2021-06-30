import pytest


# noinspection PyPep8Naming
@pytest.mark.django_db
def test_migration_fixes_duplicate_field_names(
    migrator, data_fixture, user_tables_in_separate_db
):
    old_state = migrator.apply_initial_migration(
        ("database", "0031_fix_url_field_max_length")
    )

    # The models used by the data_fixture below are not touched by this migration so
    # it is safe to use the latest version in the test.
    user = data_fixture.create_user()
    database = data_fixture.create_database_application(user=user)

    Table = old_state.apps.get_model("database", "Table")
    ContentType = old_state.apps.get_model("contenttypes", "ContentType")
    table = Table.objects.create(database_id=database.id, name="test", order=0)
    other_table = Table.objects.create(database_id=database.id, name="test", order=1)

    TextField = old_state.apps.get_model("database", "TextField")
    Field = old_state.apps.get_model("database", "Field")
    content_type_id = ContentType.objects.get_for_model(TextField).id
    first_dupe_field = Field.objects.create(
        name="Duplicate",
        table_id=table.id,
        primary=True,
        order=1,
        content_type_id=content_type_id,
    )
    second_dupe_field = Field.objects.create(
        name="Duplicate",
        table_id=table.id,
        order=2,
        primary=False,
        content_type_id=content_type_id,
    )
    dupe_field_but_in_other_table = Field.objects.create(
        name="Duplicate",
        table_id=other_table.id,
        order=2,
        primary=False,
        content_type_id=content_type_id,
    )
    first_dupe_in_other_table = Field.objects.create(
        name="Other",
        table_id=other_table.id,
        order=2,
        primary=False,
        content_type_id=content_type_id,
    )
    second_dupe_in_other_table = Field.objects.create(
        name="Other",
        table_id=other_table.id,
        order=2,
        primary=False,
        content_type_id=content_type_id,
    )
    third_dupe_in_other_table = Field.objects.create(
        name="Other",
        table_id=other_table.id,
        order=2,
        primary=False,
        content_type_id=content_type_id,
    )

    new_state = migrator.apply_tested_migration(("database", "0032_unique_field_names"))
    # After the initial migration is done, we can use the model state:
    Field = new_state.apps.get_model("database", "Field")
    assert Field.objects.get(id=first_dupe_field.id).name == "Duplicate"
    assert Field.objects.get(id=first_dupe_field.id).old_name is None
    assert Field.objects.get(id=second_dupe_field.id).name == "Duplicate_2"
    assert Field.objects.get(id=second_dupe_field.id).old_name == "Duplicate"
    assert Field.objects.get(id=dupe_field_but_in_other_table.id).name == "Duplicate"
    assert Field.objects.get(id=dupe_field_but_in_other_table.id).old_name is None
    assert Field.objects.get(id=first_dupe_in_other_table.id).name == "Other"
    assert Field.objects.get(id=first_dupe_in_other_table.id).old_name is None
    assert Field.objects.get(id=second_dupe_in_other_table.id).name == "Other_2"
    assert Field.objects.get(id=second_dupe_in_other_table.id).old_name == "Other"
    assert Field.objects.get(id=third_dupe_in_other_table.id).name == "Other_3"
    assert Field.objects.get(id=third_dupe_in_other_table.id).old_name == "Other"


# noinspection PyPep8Naming
@pytest.mark.django_db
def test_migration_handles_existing_fields_with_underscore_number(
    migrator, data_fixture, user_tables_in_separate_db
):
    old_state = migrator.apply_initial_migration(
        ("database", "0031_fix_url_field_max_length")
    )

    # The models used by the data_fixture below are not touched by this migration so
    # it is safe to use the latest version in the test.
    user = data_fixture.create_user()
    database = data_fixture.create_database_application(user=user)

    Table = old_state.apps.get_model("database", "Table")
    ContentType = old_state.apps.get_model("contenttypes", "ContentType")
    table = Table.objects.create(database_id=database.id, name="test", order=0)

    TextField = old_state.apps.get_model("database", "TextField")
    Field = old_state.apps.get_model("database", "Field")
    content_type_id = ContentType.objects.get_for_model(TextField).id
    first_dupe_field = Field.objects.create(
        name="Duplicate",
        table_id=table.id,
        primary=True,
        order=1,
        content_type_id=content_type_id,
    )
    second_dupe_field = Field.objects.create(
        name="Duplicate",
        table_id=table.id,
        order=2,
        primary=False,
        content_type_id=content_type_id,
    )
    existing_field_with_clashing_name_after_dedupe = Field.objects.create(
        name="Duplicate_2",
        table_id=table.id,
        order=2,
        primary=False,
        content_type_id=content_type_id,
    )
    new_state = migrator.apply_tested_migration(("database", "0032_unique_field_names"))

    Field = new_state.apps.get_model("database", "Field")
    assert Field.objects.get(id=first_dupe_field.id).name == "Duplicate"
    assert Field.objects.get(id=first_dupe_field.id).old_name is None
    assert Field.objects.get(id=second_dupe_field.id).name == "Duplicate_3"
    assert Field.objects.get(id=second_dupe_field.id).old_name == "Duplicate"
    clash = Field.objects.get(id=existing_field_with_clashing_name_after_dedupe.id)
    assert clash.name == "Duplicate_2"
    assert clash.old_name is None


# noinspection PyPep8Naming
@pytest.mark.django_db
def test_backwards_migration_restores_field_names(
    migrator, data_fixture, user_tables_in_separate_db
):
    old_state = migrator.apply_initial_migration(
        ("database", "0032_unique_field_names")
    )

    # The models used by the data_fixture below are not touched by this migration so
    # it is safe to use the latest version in the test.
    user = data_fixture.create_user()
    database = data_fixture.create_database_application(user=user)

    Table = old_state.apps.get_model("database", "Table")
    ContentType = old_state.apps.get_model("contenttypes", "ContentType")
    table = Table.objects.create(database_id=database.id, name="test", order=0)

    TextField = old_state.apps.get_model("database", "TextField")
    Field = old_state.apps.get_model("database", "Field")
    content_type_id = ContentType.objects.get_for_model(TextField).id
    first_dupe_field = Field.objects.create(
        name="Duplicate",
        old_name=None,
        table_id=table.id,
        primary=True,
        order=1,
        content_type_id=content_type_id,
    )
    second_dupe_field = Field.objects.create(
        name="Duplicate_2",
        old_name="Duplicate",
        table_id=table.id,
        order=2,
        primary=False,
        content_type_id=content_type_id,
    )
    third_dupe_field = Field.objects.create(
        name="Duplicate_3",
        old_name="Duplicate",
        table_id=table.id,
        order=2,
        primary=False,
        content_type_id=content_type_id,
    )
    new_state = migrator.apply_tested_migration(
        ("database", "0031_fix_url_field_max_length")
    )

    Field = new_state.apps.get_model("database", "Field")
    assert Field.objects.get(id=first_dupe_field.id).name == "Duplicate"
    assert Field.objects.get(id=second_dupe_field.id).name == "Duplicate"
    assert Field.objects.get(id=third_dupe_field.id).name == "Duplicate"


# noinspection PyPep8Naming
@pytest.mark.django_db
def test_migration_fixes_duplicate_field_names_and_reserved_names(
    migrator, data_fixture, user_tables_in_separate_db
):
    old_state = migrator.apply_initial_migration(
        ("database", "0031_fix_url_field_max_length")
    )

    # The models used by the data_fixture below are not touched by this migration so
    # it is safe to use the latest version in the test.
    user = data_fixture.create_user()
    database = data_fixture.create_database_application(user=user)

    Table = old_state.apps.get_model("database", "Table")
    ContentType = old_state.apps.get_model("contenttypes", "ContentType")
    table = Table.objects.create(database_id=database.id, name="test", order=0)
    other_table = Table.objects.create(database_id=database.id, name="test", order=1)

    TextField = old_state.apps.get_model("database", "TextField")
    Field = old_state.apps.get_model("database", "Field")
    content_type_id = ContentType.objects.get_for_model(TextField).id
    first_dupe_field = Field.objects.create(
        name="Duplicate",
        table_id=table.id,
        primary=True,
        order=1,
        content_type_id=content_type_id,
    )
    second_dupe_field = Field.objects.create(
        name="Duplicate",
        table_id=table.id,
        order=2,
        primary=False,
        content_type_id=content_type_id,
    )
    reserved_field_1 = Field.objects.create(
        name="id",
        table_id=table.id,
        order=2,
        primary=False,
        content_type_id=content_type_id,
    )
    reserved_field_2 = Field.objects.create(
        name="id",
        table_id=table.id,
        order=2,
        primary=False,
        content_type_id=content_type_id,
    )
    blank_in_other_table = Field.objects.create(
        name="",
        table_id=other_table.id,
        order=2,
        primary=False,
        content_type_id=content_type_id,
    )
    reserved_in_other_table_1 = Field.objects.create(
        name="order",
        table_id=other_table.id,
        order=2,
        primary=False,
        content_type_id=content_type_id,
    )
    reserved_in_other_table_2 = Field.objects.create(
        name="order",
        table_id=other_table.id,
        order=2,
        primary=False,
        content_type_id=content_type_id,
    )

    normal_field_1 = Field.objects.create(
        name="Order",
        table_id=other_table.id,
        order=2,
        primary=False,
        content_type_id=content_type_id,
    )
    normal_field_2 = Field.objects.create(
        name="Id",
        table_id=other_table.id,
        order=2,
        primary=False,
        content_type_id=content_type_id,
    )
    new_state = migrator.apply_tested_migration(("database", "0032_unique_field_names"))
    # After the initial migration is done, we can use the model state:
    Field = new_state.apps.get_model("database", "Field")
    assert Field.objects.get(id=first_dupe_field.id).name == "Duplicate"
    assert Field.objects.get(id=first_dupe_field.id).old_name is None
    assert Field.objects.get(id=second_dupe_field.id).name == "Duplicate_2"
    assert Field.objects.get(id=second_dupe_field.id).old_name == "Duplicate"
    assert Field.objects.get(id=reserved_field_1.id).name == "id_2"
    assert Field.objects.get(id=reserved_field_1.id).old_name == "id"
    assert Field.objects.get(id=reserved_field_2.id).name == "id_3"
    assert Field.objects.get(id=reserved_field_2.id).old_name == "id"
    assert Field.objects.get(id=blank_in_other_table.id).name == "Field_1"
    assert Field.objects.get(id=blank_in_other_table.id).old_name == ""
    assert Field.objects.get(id=reserved_in_other_table_1.id).name == "order_2"
    assert Field.objects.get(id=reserved_in_other_table_1.id).old_name == "order"
    assert Field.objects.get(id=reserved_in_other_table_2.id).name == "order_3"
    assert Field.objects.get(id=reserved_in_other_table_2.id).old_name == "order"
    assert Field.objects.get(id=normal_field_1.id).name == "Order"
    assert Field.objects.get(id=normal_field_1.id).old_name is None
    assert Field.objects.get(id=normal_field_2.id).name == "Id"
    assert Field.objects.get(id=normal_field_2.id).old_name is None
