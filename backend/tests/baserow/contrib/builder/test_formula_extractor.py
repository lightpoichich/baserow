from typing import List
from unittest.mock import patch

import pytest

from baserow.contrib.builder.formula_property_extractor import (
    get_data_source_field_names,
    get_element_field_names,
    get_formula_field_names,
    get_workflow_action_field_names,
)
from baserow.contrib.builder.workflow_actions.models import EventTypes
from baserow.contrib.builder.workflow_actions.service import (
    BuilderWorkflowActionService,
)
from baserow.contrib.builder.workflow_actions.workflow_action_types import (
    CreateRowWorkflowActionType,
    DeleteRowWorkflowActionType,
    NotificationWorkflowActionType,
    OpenPageWorkflowActionType,
    UpdateRowWorkflowActionType,
)
from baserow.core.formula.parser.exceptions import BaserowFormulaSyntaxError
from baserow.core.formula.registries import DataProviderType
from baserow.core.formula.runtime_formula_context import RuntimeFormulaContext


class TestDataProviderType(DataProviderType):
    type = "test_provider"

    def get_data_chunk(
        self, runtime_formula_context: RuntimeFormulaContext, path: List[str]
    ):
        return super().get_data_chunk(runtime_formula_context, path)


@pytest.mark.django_db
def test_get_formula_field_names_returns_empty_list(data_fixture):
    """
    Test the get_formula_field_names() function.

    Ensure that an empty dict is returned if no Elements are found.
    """

    user = data_fixture.create_user()
    page = data_fixture.create_builder_page(user=user)

    results = get_formula_field_names(user, page)

    assert results == {
        "all": {},
        "external": {},
        "internal": {},
    }


@pytest.mark.django_db
def test_get_formula_field_names_returns_all_field_names(data_fixture):
    """
    Test the get_formula_field_names() function.

    Ensure that all the expected field names are returned.
    """

    user = data_fixture.create_user()
    workspace = data_fixture.create_workspace(user=user)
    table, fields, rows = data_fixture.build_table(
        user=user,
        columns=[
            ("Food", "text"),
            ("Spiciness", "number"),
        ],
        rows=[
            ["Paneer Tikka", 5],
            ["Gobi Manchurian", 8],
        ],
    )
    builder = data_fixture.create_builder_application(user=user, workspace=workspace)
    integration = data_fixture.create_local_baserow_integration(
        user=user, application=builder
    )
    page = data_fixture.create_builder_page(user=user)
    data_source = data_fixture.create_builder_local_baserow_list_rows_data_source(
        user=user,
        page=page,
        integration=integration,
        table=table,
    )
    data_fixture.create_builder_table_element(
        user=user,
        page=page,
        data_source=data_source,
        fields=[
            {
                "name": "FieldA",
                "type": "text",
                "config": {"value": f"get('current_record.field_{fields[0].id}')"},
            },
            {
                "name": "FieldB",
                "type": "text",
                "config": {"value": f"get('current_record.field_{fields[1].id}')"},
            },
        ],
    )

    results = get_formula_field_names(user, page)

    assert sorted(list(results)) == ["all", "external", "internal"]
    assert sorted(results["all"][data_source.service_id]) == [
        f"field_{field.id}" for field in fields
    ]
    assert sorted(results["external"][data_source.service_id]) == [
        f"field_{field.id}" for field in fields
    ]
    assert results["internal"] == {}


@pytest.mark.django_db
def test_get_formula_field_names_returns_some_field_names(data_fixture):
    """
    Test the get_formula_field_names() function.

    Ensure that only some of the field names are returned. A field name should
    only be returned if it is used in the page.
    """

    user = data_fixture.create_user()
    workspace = data_fixture.create_workspace(user=user)
    table, fields, rows = data_fixture.build_table(
        user=user,
        columns=[
            ("Food", "text"),
            ("Spiciness", "number"),
        ],
        rows=[
            ["Paneer Tikka", 5],
            ["Gobi Manchurian", 8],
        ],
    )
    builder = data_fixture.create_builder_application(user=user, workspace=workspace)
    integration = data_fixture.create_local_baserow_integration(
        user=user, application=builder
    )
    page = data_fixture.create_builder_page(user=user)
    data_source = data_fixture.create_builder_local_baserow_list_rows_data_source(
        user=user,
        page=page,
        integration=integration,
        table=table,
    )
    data_fixture.create_builder_table_element(
        user=user,
        page=page,
        data_source=data_source,
        fields=[
            # Although there are two fields, this Table element only uses one.
            {
                "name": "FieldA",
                "type": "text",
                "config": {"value": f"get('current_record.field_{fields[0].id}')"},
            },
        ],
    )

    results = get_formula_field_names(user, page)

    # Since the Table element (which is the only element in the Page) uses
    # only one field, ensure that specific field is the only one returned.
    assert results == {
        "all": {
            data_source.service_id: [f"field_{fields[0].id}"],
        },
        "external": {
            data_source.service_id: [f"field_{fields[0].id}"],
        },
        "internal": {},
    }


def test_extract_properties_returns_none():
    """
    Ensure the default implementation of extract_properties() returns {}.
    """

    assert TestDataProviderType().extract_properties([]) == {}


@patch("baserow.contrib.builder.mixins.get_parse_tree_for_formula")
def test_get_element_field_names_returns_empty_if_no_elements(mock_parse_tree):
    """
    Ensure the get_element_field_names() function returns an empty dict if
    there are no elements.
    """

    results = get_element_field_names([], {})

    assert results == {"external": {}}
    mock_parse_tree.assert_not_called()


@pytest.mark.django_db
@patch("baserow.contrib.builder.mixins.get_parse_tree_for_formula")
def test_get_element_field_names_returns_empty_if_no_formulas(
    mock_parse_tree, data_fixture
):
    """
    Ensure the get_element_field_names() function returns an empty dict if
    the element has no formula.
    """

    user = data_fixture.create_user()
    builder = data_fixture.create_builder_application(user=user)
    page = data_fixture.create_builder_page(user=user, builder=builder)

    heading_element_1 = data_fixture.create_builder_heading_element(page=page, value="")
    heading_element_2 = data_fixture.create_builder_heading_element(page=page, value="")

    results = get_element_field_names([heading_element_1, heading_element_2], {})

    assert results == {"external": {}}
    mock_parse_tree.assert_not_called()


@pytest.mark.django_db
@patch("baserow.contrib.builder.mixins.get_parse_tree_for_formula")
def test_get_element_field_names_returns_empty_if_invalid_formula(
    mock_parse_tree, data_fixture
):
    """
    Ensure the get_element_field_names() function returns an empty dict if
    the elements has an invalid formula.
    """

    user = data_fixture.create_user()
    builder = data_fixture.create_builder_application(user=user)
    page = data_fixture.create_builder_page(user=user, builder=builder)

    heading_element = data_fixture.create_builder_heading_element(
        page=page, value="foo"
    )

    # Simulate an "invalid formula" error
    mock_parse_tree.side_effect = BaserowFormulaSyntaxError("Invalid formula!")

    result = get_element_field_names([heading_element], {})

    assert result == {"external": {}}
    mock_parse_tree.assert_called_once_with("foo")


@pytest.mark.django_db
def test_get_element_field_names_returns_field_names(data_fixture):
    """
    Ensure the get_element_field_names() function returns the expected field names.
    """

    user = data_fixture.create_user()
    table, fields, _ = data_fixture.build_table(
        user=user,
        columns=[
            ("Fruit", "text"),
            ("Color", "text"),
            ("Country", "text"),
        ],
        rows=[
            ["Apple", "Green", "China"],
            ["Banana", "Yellow", "Ecuador"],
            ["Cherry", "Red", "Turkey"],
        ],
    )
    builder = data_fixture.create_builder_application(user=user)
    page = data_fixture.create_builder_page(user=user, builder=builder)
    data_source_1 = data_fixture.create_builder_local_baserow_list_rows_data_source(
        user=user,
        page=page,
        table=table,
    )
    data_source_2 = data_fixture.create_builder_local_baserow_list_rows_data_source(
        user=user,
        page=page,
        table=table,
    )

    heading_element_1 = data_fixture.create_builder_heading_element(
        page=page,
        value=f"get('data_source.{data_source_1.id}.0.field_{fields[0].id}')",
    )
    heading_element_2 = data_fixture.create_builder_heading_element(
        page=page,
        value=f"get('data_source.{data_source_1.id}.0.field_{fields[1].id}')",
    )
    heading_element_3 = data_fixture.create_builder_heading_element(
        page=page,
        value=f"get('data_source.{data_source_2.id}.0.field_{fields[2].id}')",
    )

    result = get_element_field_names(
        [heading_element_1, heading_element_2, heading_element_3],
        {},
    )

    assert list(result) == ["external"]
    assert sorted(list(result["external"])) == [
        data_source_1.service.id,
        data_source_2.service.id,
    ]
    assert sorted(list(result["external"][data_source_1.service.id])) == [
        # Since only the first two fields are used by elements in this page,
        # we expect to see _only_ those two fields.
        f"field_{fields[0].id}",
        f"field_{fields[1].id}",
    ]
    assert sorted(list(result["external"][data_source_2.service.id])) == [
        f"field_{fields[2].id}",
    ]


@pytest.mark.django_db
@patch("baserow.contrib.builder.mixins.get_parse_tree_for_formula")
def test_get_workflow_action_field_names_returns_empty_if_no_workflow_actions(
    mock_parse_tree, data_fixture
):
    """
    Ensure the get_workflow_action_field_names() function returns an empty dict if
    there are no workflow actions.
    """

    user = data_fixture.create_user()
    builder = data_fixture.create_builder_application(user=user)
    page = data_fixture.create_builder_page(user=user, builder=builder)

    results = get_workflow_action_field_names(user, page, {})

    assert results == {"internal": {}, "external": {}}

    mock_parse_tree.assert_not_called()


@pytest.mark.django_db
@patch("baserow.contrib.builder.mixins.get_parse_tree_for_formula")
def test_get_workflow_action_field_names_returns_empty_if_no_formulas(
    mock_parse_tree, data_fixture
):
    """
    Ensure the get_workflow_action_field_names() function returns an empty dict if
    the workflow action has no formula.
    """

    user = data_fixture.create_user()
    builder = data_fixture.create_builder_application(user=user)
    page = data_fixture.create_builder_page(user=user, builder=builder)

    button_element = data_fixture.create_builder_button_element(page=page)
    workflow_action = (
        BuilderWorkflowActionService()
        .create_workflow_action(
            user,
            NotificationWorkflowActionType(),
            page=page,
            element=button_element,
            event=EventTypes.CLICK,
            description="",
        )
        .specific
    )

    results = get_workflow_action_field_names(user, page, {})

    assert results == {"external": {}, "internal": {}}
    mock_parse_tree.assert_not_called()


@pytest.mark.django_db
@patch("baserow.contrib.builder.mixins.get_parse_tree_for_formula")
def test_get_workflow_action_field_names_returns_empty_if_invalid_formula(
    mock_parse_tree, data_fixture
):
    """
    Ensure the get_workflow_action_field_names() function returns an empty dict if
    the workflow action has an invalid formula.
    """

    user = data_fixture.create_user()
    builder = data_fixture.create_builder_application(user=user)
    page = data_fixture.create_builder_page(user=user, builder=builder)

    button_element = data_fixture.create_builder_button_element(page=page)
    workflow_action = (
        BuilderWorkflowActionService()
        .create_workflow_action(
            user,
            NotificationWorkflowActionType(),
            page=page,
            element=button_element,
            event=EventTypes.CLICK,
            description="foo",
        )
        .specific
    )

    # Simulate an "invalid formula" error
    mock_parse_tree.side_effect = BaserowFormulaSyntaxError("Invalid formula!")

    results = get_workflow_action_field_names(user, page, {})

    assert results == {"external": {}, "internal": {}}
    mock_parse_tree.assert_called_once_with("foo")


@pytest.mark.django_db
def test_get_workflow_action_field_names_returns_field_names(data_fixture):
    """
    Ensure the get_workflow_action_field_names() function returns field names.
    """

    user = data_fixture.create_user()
    table, fields, _ = data_fixture.build_table(
        user=user,
        columns=[
            ("Fruit", "text"),
            ("Color", "text"),
            ("Country", "text"),
        ],
        rows=[
            ["Apple", "Green", "China"],
            ["Banana", "Yellow", "Ecuador"],
            ["Cherry", "Red", "Turkey"],
        ],
    )
    builder = data_fixture.create_builder_application(user=user)
    page = data_fixture.create_builder_page(user=user, builder=builder)
    data_source_1 = data_fixture.create_builder_local_baserow_list_rows_data_source(
        user=user,
        page=page,
        table=table,
    )
    data_source_2 = data_fixture.create_builder_local_baserow_list_rows_data_source(
        user=user,
        page=page,
        table=table,
    )

    button_element = data_fixture.create_builder_button_element(page=page)
    workflow_action = (
        BuilderWorkflowActionService()
        .create_workflow_action(
            user,
            NotificationWorkflowActionType(),
            page=page,
            element=button_element,
            event=EventTypes.CLICK,
            title=f"get('data_source.{data_source_1.id}.1.field_{fields[0].id}')",
            description=f"get('data_source.{data_source_2.id}.1.field_{fields[1].id}')",
        )
        .specific
    )

    results = get_workflow_action_field_names(user, page, {})

    assert sorted(list(results)) == ["external", "internal"]
    # Since the third field is not used anywhere in the page, we do _not_
    # expect to see that field in the results.
    assert sorted(list(results["external"][data_source_1.service.id])) == [
        f"field_{fields[0].id}"
    ]
    assert sorted(list(results["external"][data_source_2.service.id])) == [
        f"field_{fields[1].id}"
    ]
    assert results["internal"] == {}


@pytest.mark.django_db
@pytest.mark.parametrize(
    "workflow_action_type,formula_fields",
    [
        [
            NotificationWorkflowActionType,
            ["title", "description"],
        ],
        [
            OpenPageWorkflowActionType,
            ["navigate_to_url"],
        ],
    ],
)
def test_get_workflow_action_field_names_returns_external_field_names(
    data_fixture, workflow_action_type, formula_fields
):
    """
    Ensure the get_workflow_action_field_names() function returns field names.

    Test that the external and internal dicts are correctly segregated.
    """

    user = data_fixture.create_user()
    table, fields, _ = data_fixture.build_table(
        user=user,
        columns=[
            ("Fruit", "text"),
            ("Color", "text"),
            ("Country", "text"),
        ],
        rows=[
            ["Apple", "Green", "China"],
            ["Banana", "Yellow", "Ecuador"],
            ["Cherry", "Red", "Turkey"],
        ],
    )
    builder = data_fixture.create_builder_application(user=user)
    page = data_fixture.create_builder_page(user=user, builder=builder)
    data_source = data_fixture.create_builder_local_baserow_list_rows_data_source(
        user=user,
        page=page,
        table=table,
    )

    button_element = data_fixture.create_builder_button_element(page=page)
    workflow_action = (
        BuilderWorkflowActionService()
        .create_workflow_action(
            user,
            workflow_action_type(),
            page=page,
            element=button_element,
            event=EventTypes.CLICK,
        )
        .specific
    )
    for field in formula_fields:
        setattr(
            workflow_action,
            field,
            f"get('data_source.{data_source.id}.1.field_{fields[0].id}')",
        )
    workflow_action.save()

    results = get_workflow_action_field_names(user, page, {})

    assert results == {
        # Since the workflow action is public/safe, only the external dict
        # should be populated.
        "external": {
            data_source.service.id: [f"field_{fields[0].id}"],
        },
        "internal": {},
    }


@pytest.mark.django_db
@pytest.mark.parametrize(
    "workflow_action_type",
    [
        CreateRowWorkflowActionType,
        DeleteRowWorkflowActionType,
        UpdateRowWorkflowActionType,
    ],
)
def test_get_workflow_action_field_names_returns_internal_field_names(
    data_fixture, workflow_action_type
):
    """
    Ensure the get_workflow_action_field_names() function returns field names.

    Test that the external and internal dicts are correctly segregated.
    """

    user = data_fixture.create_user()
    table, fields, _ = data_fixture.build_table(
        user=user,
        columns=[
            ("Fruit", "text"),
            ("Color", "text"),
            ("Country", "text"),
        ],
        rows=[
            ["Apple", "Green", "China"],
            ["Banana", "Yellow", "Ecuador"],
            ["Cherry", "Red", "Turkey"],
        ],
    )
    builder = data_fixture.create_builder_application(user=user)
    page = data_fixture.create_builder_page(user=user, builder=builder)
    data_source = data_fixture.create_builder_local_baserow_list_rows_data_source(
        user=user,
        page=page,
        table=table,
    )

    button_element = data_fixture.create_builder_button_element(page=page)
    workflow_action = (
        BuilderWorkflowActionService()
        .create_workflow_action(
            user,
            workflow_action_type(),
            page=page,
            element=button_element,
            event=EventTypes.CLICK,
        )
        .specific
    )
    workflow_action.service.row_id = (
        f"get('data_source.{data_source.id}.1.field_{fields[0].id}')"
    )
    workflow_action.service.save()

    results = get_workflow_action_field_names(user, page, {})

    assert results == {
        "external": {},
        # Since the workflow action is public/safe, only the external dict
        # should be populated.
        "internal": {
            data_source.service.id: [f"field_{fields[0].id}"],
        },
    }


@pytest.mark.django_db
@patch("baserow.contrib.builder.mixins.get_parse_tree_for_formula")
def test_get_data_source_field_names_returns_empty_if_no_data_sources(
    mock_parse_tree, data_fixture
):
    """
    Ensure the get_data_source_field_names() function returns an empty dict if
    there are no data sources.
    """

    user = data_fixture.create_user()
    builder = data_fixture.create_builder_application(user=user)
    page = data_fixture.create_builder_page(user=user, builder=builder)

    result = get_data_source_field_names(page)

    assert result == {"internal": {}}
    mock_parse_tree.assert_not_called()


@pytest.mark.django_db
@patch("baserow.contrib.builder.mixins.get_parse_tree_for_formula")
def test_get_data_source_field_names_returns_empty_if_invalid_formula(
    mock_parse_tree, data_fixture
):
    """
    Ensure the get_data_source_field_names() function returns an empty dict if
    the data source has an invalid formula.
    """

    user = data_fixture.create_user()
    table, fields, _ = data_fixture.build_table(
        user=user,
        columns=[
            ("Fruit", "text"),
            ("Color", "text"),
            ("Country", "text"),
        ],
        rows=[
            ["Apple", "Green", "China"],
            ["Banana", "Yellow", "Ecuador"],
            ["Cherry", "Red", "Turkey"],
        ],
    )
    builder = data_fixture.create_builder_application(user=user)
    integration = data_fixture.create_local_baserow_integration(
        application=builder, user=user
    )
    page = data_fixture.create_builder_page(user=user, builder=builder)

    list_rows_service = data_fixture.create_local_baserow_list_rows_service(
        integration=integration,
        search_query="foo",
    )

    data_fixture.create_builder_local_baserow_list_rows_data_source(
        user=user,
        page=page,
        table=table,
        service=list_rows_service,
    )

    # Simulate an "invalid formula" error
    mock_parse_tree.side_effect = BaserowFormulaSyntaxError("Invalid formula!")

    results = get_data_source_field_names(page)

    assert results == {"internal": {}}
    mock_parse_tree.assert_called_once_with("foo")


@pytest.mark.django_db
def test_get_data_source_field_names_list_rows_returns_field_names(data_fixture):
    """
    Ensure the get_data_source_field_names() function returns the expected
    field_names for the List Rows service type.
    """

    user = data_fixture.create_user()
    table, fields, _ = data_fixture.build_table(
        user=user,
        columns=[
            ("Fruit", "text"),
            ("Color", "text"),
            ("Country", "text"),
        ],
        rows=[
            ["Apple", "Green", "China"],
            ["Banana", "Yellow", "Ecuador"],
            ["Cherry", "Red", "Turkey"],
        ],
    )
    builder = data_fixture.create_builder_application(user=user)
    integration = data_fixture.create_local_baserow_integration(
        application=builder, user=user
    )
    page = data_fixture.create_builder_page(user=user, builder=builder)

    list_rows_service = data_fixture.create_local_baserow_list_rows_service(
        integration=integration,
    )

    data_source_1 = data_fixture.create_builder_local_baserow_list_rows_data_source(
        user=user,
        page=page,
        table=table,
    )

    data_source_2 = data_fixture.create_builder_local_baserow_list_rows_data_source(
        user=user,
        page=page,
        table=table,
        service=list_rows_service,
    )
    list_rows_service.search_query = (
        f"get('data_source.{data_source_1.id}.0.field_{fields[0].id}')"
    )
    list_rows_service.save()

    results = get_data_source_field_names(page)

    assert list(results) == ["internal"]
    assert sorted(list(results["internal"][data_source_1.service.id])) == [
        f"field_{fields[0].id}"
    ]


@pytest.mark.django_db
def test_get_data_source_field_names_get_row_returns_field_names(data_fixture):
    """
    Ensure the get_data_source_field_names() function returns the expected
    field_names for the Get Row service type.
    """

    user = data_fixture.create_user()
    table, fields, _ = data_fixture.build_table(
        user=user,
        columns=[
            ("Fruit", "text"),
            ("Color", "text"),
            ("Country", "text"),
        ],
        rows=[
            ["Apple", "Green", "China"],
            ["Banana", "Yellow", "Ecuador"],
            ["Cherry", "Red", "Turkey"],
        ],
    )
    builder = data_fixture.create_builder_application(user=user)
    integration = data_fixture.create_local_baserow_integration(
        application=builder, user=user
    )
    page = data_fixture.create_builder_page(user=user, builder=builder)

    get_row_service = data_fixture.create_local_baserow_get_row_service(
        integration=integration
    )

    data_source_1 = data_fixture.create_builder_local_baserow_list_rows_data_source(
        user=user,
        page=page,
        table=table,
    )

    data_source_2 = data_fixture.create_builder_local_baserow_get_row_data_source(
        user=user,
        page=page,
        table=table,
        service=get_row_service,
    )
    get_row_service.row_id = (
        f"get('data_source.{data_source_1.id}.0.field_{fields[1].id}')"
    )
    get_row_service.save()

    results = get_data_source_field_names(page)

    assert results == {
        "internal": {data_source_1.service.id: [f"field_{fields[1].id}"]},
    }


@pytest.mark.django_db
@patch("baserow.contrib.builder.mixins.get_parse_tree_for_formula")
def test_get_data_source_field_names_skips_if_no_service(mock_parse_tree, data_fixture):
    """
    Ensure the get_data_source_field_names() function skips processing a
    Data Source if its service is not configured.

    The user can create a Data Source and not fully configure it. Thus it is
    important that the code doesn't assume a Data Source always has a Service.
    """

    user = data_fixture.create_user()
    table, _, _ = data_fixture.build_table(
        user=user,
        columns=[
            ("Fruit", "text"),
        ],
        rows=[
            ["Apple", "Green", "China"],
        ],
    )
    builder = data_fixture.create_builder_application(user=user)
    page = data_fixture.create_builder_page(user=user, builder=builder)

    # Create a Data Source, but don't create a Service
    data_source = data_fixture.create_builder_local_baserow_list_rows_data_source(
        user=user,
        page=page,
        table=table,
    )
    data_source.service = None
    data_source.save()

    results = get_data_source_field_names(page)

    assert results == {"internal": {}}
    mock_parse_tree.assert_not_called()
