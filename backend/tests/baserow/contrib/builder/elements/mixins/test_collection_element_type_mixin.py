"""
Test the CollectionElementTypeMixin class.
"""
import json
from io import BytesIO
from unittest.mock import MagicMock

import pytest

from baserow.contrib.builder.elements.mixins import CollectionElementTypeMixin
from baserow.core.handler import CoreHandler
from baserow.core.registries import ImportExportConfig

MODULE_PATH = "baserow.contrib.builder.elements.collection_field_types"


@pytest.mark.parametrize(
    "schema_property",
    [
        "field_123",
        None,
    ],
)
def test_import_context_addition_sets_schema_property(schema_property):
    """
    Test the import_context_addition() method.

    Ensure that the schema_property is set when the element has a schema property.
    """

    data_source_id = 100

    mock_element = MagicMock()
    mock_element.schema_property = schema_property
    mock_element.data_source_id = data_source_id

    result = CollectionElementTypeMixin().import_context_addition(mock_element)

    assert result["data_source_id"] == data_source_id
    if schema_property:
        assert result["schema_property"] == schema_property
    else:
        assert "schema_property" not in result


@pytest.mark.django_db(transaction=True)
def test_import_export_collection_element_type(data_fixture):
    user = data_fixture.create_user()
    workspace = data_fixture.create_workspace(user=user)
    builder = data_fixture.create_builder_application(workspace=workspace)
    page = data_fixture.create_builder_page(builder=builder)
    database = data_fixture.create_database_application(workspace=workspace)
    table = data_fixture.create_database_table(database=database)
    field = data_fixture.create_text_field(table=table)
    element = data_fixture.create_builder_table_element(
        page=page,
        fields=[
            {
                "name": "Name",
                "type": "text",
                "config": {"value": f"'foobar'"},
            },
        ],
    )
    element.property_options.create(schema_property=field.db_column, sortable=True)

    config = ImportExportConfig(include_permission_data=False)
    exported_applications = CoreHandler().export_workspace_applications(
        workspace, BytesIO(), config
    )

    # Ensure the values are json serializable
    try:
        json.dumps(exported_applications)
    except Exception as e:
        pytest.fail(f"Exported applications are not json serializable: {e}")

    imported_applications, _ = CoreHandler().import_applications_to_workspace(
        workspace, exported_applications, BytesIO(), config, None
    )
    imported_database, imported_builder = imported_applications

    # Pluck out the imported database records.
    imported_table = imported_database.table_set.get()
    imported_field = imported_table.field_set.get()

    # Pluck out the imported builder records.
    imported_page = imported_builder.page_set.exclude(path="__shared__")[0]
    imported_element = imported_page.element_set.get()
    imported_property_option = imported_element.property_options.get()

    assert imported_property_option.schema_property == imported_field.db_column
