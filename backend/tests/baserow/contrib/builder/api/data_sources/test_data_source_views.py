import json
from unittest.mock import ANY, MagicMock, patch

from django.urls import reverse

import pytest
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_404_NOT_FOUND,
)

from baserow.contrib.builder.data_sources.models import DataSource
from baserow.contrib.builder.elements.models import Element
from baserow.core.services.models import Service
from baserow.core.user_sources.registries import user_source_type_registry
from baserow.core.user_sources.user_source_user import UserSourceUser
from baserow.test_utils.helpers import AnyStr


@pytest.mark.django_db
def test_get_data_sources(api_client, data_fixture):
    user, token = data_fixture.create_user_and_token()
    page = data_fixture.create_builder_page(user=user)
    data_source1 = data_fixture.create_builder_local_baserow_get_row_data_source(
        page=page
    )
    data_source2 = data_fixture.create_builder_local_baserow_get_row_data_source(
        page=page
    )
    data_source3 = data_fixture.create_builder_local_baserow_list_rows_data_source(
        page=page
    )

    url = reverse("api:builder:data_source:list", kwargs={"page_id": page.id})
    response = api_client.get(
        url,
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )

    response_json = response.json()
    assert response.status_code == HTTP_200_OK
    assert len(response_json) == 3
    assert response_json[0]["id"] == data_source1.id
    assert response_json[0]["type"] == "local_baserow_get_row"
    assert "row_id" in response_json[0]
    assert response_json[1]["id"] == data_source2.id
    assert response_json[1]["type"] == "local_baserow_get_row"
    assert response_json[2]["id"] == data_source3.id
    assert response_json[2]["type"] == "local_baserow_list_rows"
    assert "row_id" not in response_json[2]


@pytest.mark.django_db
def test_create_data_source(api_client, data_fixture):
    user, token = data_fixture.create_user_and_token()
    page = data_fixture.create_builder_page(user=user)

    url = reverse("api:builder:data_source:list", kwargs={"page_id": page.id})
    response = api_client.post(
        url,
        {"type": "local_baserow_get_row"},
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )

    response_json = response.json()
    assert response.status_code == HTTP_200_OK
    assert response_json["type"] == "local_baserow_get_row"
    assert response_json["view_id"] is None
    assert response_json["table_id"] is None

    table = data_fixture.create_database_table(user=user)

    response = api_client.post(
        url,
        {
            "type": "local_baserow_get_row",
            "table_id": table.id,
        },
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )

    response_json = response.json()
    assert response.status_code == HTTP_200_OK
    assert response_json["table_id"] == table.id
    assert response_json["view_id"] is None


@pytest.mark.django_db
def test_create_data_source_bad_request(api_client, data_fixture):
    user, token = data_fixture.create_user_and_token()
    page = data_fixture.create_builder_page(user=user)

    url = reverse("api:builder:data_source:list", kwargs={"page_id": page.id})
    response = api_client.post(
        url,
        {"type": "local_baserow_get_row", "table_id": []},
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )

    response_json = response.json()
    assert response.status_code == HTTP_400_BAD_REQUEST
    assert response_json["error"] == "ERROR_REQUEST_BODY_VALIDATION"


@pytest.mark.django_db
def test_create_data_source_permission_denied(
    api_client, data_fixture, stub_check_permissions
):
    user, token = data_fixture.create_user_and_token()
    page = data_fixture.create_builder_page(user=user)

    url = reverse("api:builder:data_source:list", kwargs={"page_id": page.id})
    with stub_check_permissions(raise_permission_denied=True):
        response = api_client.post(
            url,
            {"type": "local_baserow_get_row"},
            format="json",
            HTTP_AUTHORIZATION=f"JWT {token}",
        )

    assert response.status_code == HTTP_401_UNAUTHORIZED
    assert response.json()["error"] == "PERMISSION_DENIED"


@pytest.mark.django_db
def test_create_data_source_page_does_not_exist(api_client, data_fixture):
    user, token = data_fixture.create_user_and_token()

    url = reverse("api:builder:data_source:list", kwargs={"page_id": 0})
    response = api_client.post(
        url,
        {"type": "local_baserow_get_row"},
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )
    assert response.status_code == HTTP_404_NOT_FOUND
    assert response.json()["error"] == "ERROR_PAGE_DOES_NOT_EXIST"


@pytest.mark.django_db
def test_update_data_source(api_client, data_fixture):
    user, token = data_fixture.create_user_and_token()
    page = data_fixture.create_builder_page(user=user)
    table = data_fixture.create_database_table(user=user)
    view = data_fixture.create_grid_view(user, table=table)
    data_source1 = data_fixture.create_builder_local_baserow_get_row_data_source(
        page=page
    )

    url = reverse(
        "api:builder:data_source:item", kwargs={"data_source_id": data_source1.id}
    )

    response = api_client.patch(
        url,
        {
            "table_id": table.id,
            "view_id": view.id,
            "row_id": '"test"',
            "name": "name test",
        },
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )
    assert response.status_code == HTTP_200_OK
    assert response.json()["view_id"] == view.id
    assert response.json()["table_id"] == table.id
    assert response.json()["row_id"] == '"test"'
    assert response.json()["name"] == "name test"


@pytest.mark.django_db
def test_update_data_source_with_filters(api_client, data_fixture):
    user, token = data_fixture.create_user_and_token()
    page = data_fixture.create_builder_page(user=user)
    table = data_fixture.create_database_table(user=user)
    text_field = data_fixture.create_text_field(table=table)
    formula_field = data_fixture.create_text_field(table=table)
    data_source1 = data_fixture.create_builder_local_baserow_get_row_data_source(
        page=page
    )

    url = reverse(
        "api:builder:data_source:item", kwargs={"data_source_id": data_source1.id}
    )

    # No existing filters, add one.
    response = api_client.patch(
        url,
        {
            "filters": [
                {
                    "field": text_field.id,
                    "type": "equals",
                    "value": "foobar",
                    "value_is_formula": False,
                },
                {
                    "field": formula_field.id,
                    "type": "equals",
                    "value": "get('page_parameter.id')",
                    "value_is_formula": True,
                },
            ]
        },
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )
    assert response.status_code == HTTP_200_OK

    service_filters = data_source1.service.service_filters.order_by("id")
    assert response.json()["filters"] == [
        {
            "id": service_filters[0].id,
            "order": service_filters[0].order,
            "field": text_field.id,
            "type": "equals",
            "value": "foobar",
            "value_is_formula": False,
        },
        {
            "id": service_filters[1].id,
            "order": service_filters[1].order,
            "field": formula_field.id,
            "type": "equals",
            "value": "get('page_parameter.id')",
            "value_is_formula": True,
        },
    ]

    # Reset the filters to nothing.
    response = api_client.patch(
        url,
        {"filters": []},
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )
    assert response.status_code == HTTP_200_OK
    assert response.json()["filters"] == []

    # Given an existing filter, we delete it if it's not in the payload.
    data_fixture.create_local_baserow_table_service_filter(
        service=data_source1.service, field=text_field, value="baz", order=0
    )
    response = api_client.patch(
        url,
        {
            "filters": [
                {
                    "service": data_source1.service_id,
                    "field": text_field.id,
                    "type": "equals",
                    "value": "foobar",
                    "value_is_formula": False,
                }
            ]
        },
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )
    assert response.status_code == HTTP_200_OK

    service_filter = data_source1.service.service_filters.get()
    assert response.json()["filters"] == [
        {
            "id": service_filter.id,
            "order": 0,
            "field": text_field.id,
            "type": "equals",
            "value": "foobar",
            "value_is_formula": False,
        }
    ]


@pytest.mark.django_db
def test_update_data_source_change_type(api_client, data_fixture):
    user, token = data_fixture.create_user_and_token()
    page = data_fixture.create_builder_page(user=user)
    data_source1 = data_fixture.create_builder_local_baserow_get_row_data_source(
        page=page
    )

    url = reverse(
        "api:builder:data_source:item", kwargs={"data_source_id": data_source1.id}
    )

    response = api_client.patch(
        url,
        {"type": "local_baserow_list_rows"},
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )

    assert response.status_code == HTTP_200_OK
    assert response.json()["type"] == "local_baserow_list_rows"

    response = api_client.patch(
        url,
        {"type": None},
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )

    assert response.status_code == HTTP_200_OK
    assert response.json()["type"] is None


@pytest.mark.django_db
def test_update_data_source_with_service_type_for_different_dispatch_type(
    api_client, data_fixture
):
    user, token = data_fixture.create_user_and_token()
    page = data_fixture.create_builder_page(user=user)
    data_source = data_fixture.create_builder_local_baserow_get_row_data_source(
        page=page
    )

    url = reverse(
        "api:builder:data_source:item", kwargs={"data_source_id": data_source.id}
    )

    response = api_client.patch(
        url,
        {"type": "local_baserow_upsert_row"},
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )

    assert response.status_code == HTTP_400_BAD_REQUEST
    assert response.json()["error"] == "ERROR_DATA_SOURCE_CANNOT_USE_SERVICE_TYPE"


@pytest.mark.django_db
def test_update_data_source_compatible_integration_is_persisted(
    api_client, data_fixture
):
    user, token = data_fixture.create_user_and_token()
    page = data_fixture.create_builder_page(user=user)
    data_source1 = data_fixture.create_builder_local_baserow_get_row_data_source(
        page=page
    )

    url = reverse(
        "api:builder:data_source:item", kwargs={"data_source_id": data_source1.id}
    )

    response = api_client.patch(
        url,
        {"type": "local_baserow_list_rows"},
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )

    response_json = response.json()
    assert response.status_code == HTTP_200_OK
    assert response_json["integration_id"] == data_source1.service.integration_id


@pytest.mark.django_db
def test_update_data_source_bad_request(api_client, data_fixture):
    user, token = data_fixture.create_user_and_token()
    page = data_fixture.create_builder_page(user=user)
    data_source1 = data_fixture.create_builder_local_baserow_get_row_data_source(
        page=page
    )

    url = reverse(
        "api:builder:data_source:item", kwargs={"data_source_id": data_source1.id}
    )
    response = api_client.patch(
        url,
        {"table_id": []},
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )
    assert response.status_code == HTTP_400_BAD_REQUEST
    assert response.json()["error"] == "ERROR_REQUEST_BODY_VALIDATION"


@pytest.mark.django_db
def test_update_data_source_does_not_exist(api_client, data_fixture):
    user, token = data_fixture.create_user_and_token()

    url = reverse("api:builder:data_source:item", kwargs={"data_source_id": 0})
    response = api_client.patch(
        url,
        {"table_id": "test"},
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )
    assert response.status_code == HTTP_404_NOT_FOUND
    assert response.json()["error"] == "ERROR_DATA_SOURCE_DOES_NOT_EXIST"


@pytest.mark.django_db
def test_move_data_source_empty_payload(api_client, data_fixture):
    user, token = data_fixture.create_user_and_token()
    page = data_fixture.create_builder_page(user=user)
    data_source1 = data_fixture.create_builder_local_baserow_get_row_data_source(
        page=page
    )
    data_source2 = data_fixture.create_builder_local_baserow_get_row_data_source(
        page=page
    )
    data_source3 = data_fixture.create_builder_local_baserow_get_row_data_source(
        page=page
    )

    url = reverse(
        "api:builder:data_source:move", kwargs={"data_source_id": data_source1.id}
    )
    response = api_client.patch(
        url,
        {},
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )
    assert response.status_code == HTTP_200_OK

    assert DataSource.objects.last().id == data_source1.id


@pytest.mark.django_db
def test_move_data_source_null_before_id(api_client, data_fixture):
    user, token = data_fixture.create_user_and_token()
    page = data_fixture.create_builder_page(user=user)
    data_source1 = data_fixture.create_builder_local_baserow_get_row_data_source(
        page=page
    )
    data_source2 = data_fixture.create_builder_local_baserow_get_row_data_source(
        page=page
    )
    data_source3 = data_fixture.create_builder_local_baserow_get_row_data_source(
        page=page
    )

    url = reverse(
        "api:builder:data_source:move", kwargs={"data_source_id": data_source1.id}
    )
    response = api_client.patch(
        url,
        {"before_id": None},
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )
    assert response.status_code == HTTP_200_OK

    assert DataSource.objects.last().id == data_source1.id


@pytest.mark.django_db
def test_move_data_source_before(api_client, data_fixture):
    user, token = data_fixture.create_user_and_token()
    page = data_fixture.create_builder_page(user=user)
    data_source1 = data_fixture.create_builder_local_baserow_get_row_data_source(
        page=page
    )
    data_source2 = data_fixture.create_builder_local_baserow_get_row_data_source(
        page=page
    )
    data_source3 = data_fixture.create_builder_local_baserow_get_row_data_source(
        page=page
    )

    url = reverse(
        "api:builder:data_source:move", kwargs={"data_source_id": data_source3.id}
    )
    response = api_client.patch(
        url,
        {"before_id": data_source2.id},
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )
    assert response.status_code == HTTP_200_OK
    assert response.json()["id"] == data_source3.id

    assert list(DataSource.objects.all())[1].id == data_source3.id


@pytest.mark.django_db
def test_move_data_source_before_not_in_same_page(api_client, data_fixture):
    user, token = data_fixture.create_user_and_token()
    page = data_fixture.create_builder_page(user=user)
    page2 = data_fixture.create_builder_page(user=user)
    data_source1 = data_fixture.create_builder_local_baserow_get_row_data_source(
        page=page
    )
    data_source2 = data_fixture.create_builder_local_baserow_get_row_data_source(
        page=page
    )
    data_source3 = data_fixture.create_builder_local_baserow_get_row_data_source(
        page=page2
    )

    url = reverse(
        "api:builder:data_source:move", kwargs={"data_source_id": data_source3.id}
    )
    response = api_client.patch(
        url,
        {"before_id": data_source2.id},
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )

    assert response.status_code == HTTP_400_BAD_REQUEST
    assert response.json()["error"] == "ERROR_DATA_SOURCE_NOT_IN_SAME_PAGE"


@pytest.mark.django_db
def test_create_data_source_with_service_type_for_different_dispatch_type(
    api_client, data_fixture
):
    user, token = data_fixture.create_user_and_token()
    page = data_fixture.create_builder_page(user=user)

    url = reverse("api:builder:data_source:list", kwargs={"page_id": page.id})
    response = api_client.post(
        url,
        {"type": "local_baserow_upsert_row"},
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )

    assert response.status_code == HTTP_400_BAD_REQUEST
    assert response.json()["error"] == "ERROR_DATA_SOURCE_CANNOT_USE_SERVICE_TYPE"


@pytest.mark.django_db
def test_move_data_source_bad_before_id(api_client, data_fixture):
    user, token = data_fixture.create_user_and_token()
    page = data_fixture.create_builder_page(user=user)
    data_source1 = data_fixture.create_builder_local_baserow_get_row_data_source(
        page=page
    )

    url = reverse(
        "api:builder:data_source:move", kwargs={"data_source_id": data_source1.id}
    )
    response = api_client.patch(
        url,
        {"before_id": 9999},
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )
    assert response.status_code == HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_delete_data_source(api_client, data_fixture):
    user, token = data_fixture.create_user_and_token()
    page = data_fixture.create_builder_page(user=user)
    data_source1 = data_fixture.create_builder_local_baserow_get_row_data_source(
        page=page
    )

    assert Service.objects.count() == 1
    url = reverse(
        "api:builder:data_source:item", kwargs={"data_source_id": data_source1.id}
    )
    response = api_client.delete(
        url,
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )
    assert response.status_code == HTTP_204_NO_CONTENT

    # Ensure the service also is deleted
    assert Service.objects.count() == 0


@pytest.mark.django_db
def test_delete_data_source_permission_denied(
    api_client, data_fixture, stub_check_permissions
):
    user, token = data_fixture.create_user_and_token()
    page = data_fixture.create_builder_page(user=user)
    data_source1 = data_fixture.create_builder_local_baserow_get_row_data_source(
        page=page
    )

    url = reverse(
        "api:builder:data_source:item", kwargs={"data_source_id": data_source1.id}
    )

    with stub_check_permissions(raise_permission_denied=True):
        response = api_client.delete(
            url,
            format="json",
            HTTP_AUTHORIZATION=f"JWT {token}",
        )

    assert response.status_code == HTTP_401_UNAUTHORIZED
    assert response.json()["error"] == "PERMISSION_DENIED"


@pytest.mark.django_db
def test_delete_data_source_data_source_not_exist(api_client, data_fixture):
    user, token = data_fixture.create_user_and_token()

    url = reverse("api:builder:data_source:item", kwargs={"data_source_id": 0})
    response = api_client.delete(
        url,
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )

    assert response.status_code == HTTP_404_NOT_FOUND
    assert response.json()["error"] == "ERROR_DATA_SOURCE_DOES_NOT_EXIST"


@pytest.mark.django_db
def test_dispatch_data_source(api_client, data_fixture):
    user, token = data_fixture.create_user_and_token()
    table, fields, rows = data_fixture.build_table(
        user=user,
        columns=[
            ("Name", "text"),
            ("My Color", "text"),
        ],
        rows=[
            ["BMW", "Blue"],
            ["Audi", "Orange"],
        ],
    )
    view = data_fixture.create_grid_view(user, table=table)
    builder = data_fixture.create_builder_application(user=user)
    integration = data_fixture.create_local_baserow_integration(
        user=user, application=builder
    )
    page = data_fixture.create_builder_page(user=user, builder=builder)
    data_source = data_fixture.create_builder_local_baserow_get_row_data_source(
        user=user,
        page=page,
        integration=integration,
        view=view,
        table=table,
        row_id="2",
    )

    url = reverse(
        "api:builder:data_source:dispatch", kwargs={"data_source_id": data_source.id}
    )

    response = api_client.post(
        url,
        {},
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )

    assert response.status_code == HTTP_200_OK
    assert response.json() == {
        "id": 2,
        "order": AnyStr(),
        fields[0].db_column: "Audi",
        fields[1].db_column: "Orange",
    }


@pytest.mark.django_db
def test_dispatch_data_source_with_adhoc_filters(api_client, data_fixture):
    user, token = data_fixture.create_user_and_token()
    table, fields, rows = data_fixture.build_table(
        user=user,
        columns=[
            ("Name", "text"),
        ],
        rows=[["Peter"], ["Afonso"], ["Tsering"], ["Jérémie"]],
    )
    view = data_fixture.create_grid_view(user, table=table)
    builder = data_fixture.create_builder_application(user=user)
    integration = data_fixture.create_local_baserow_integration(
        user=user, application=builder
    )
    page = data_fixture.create_builder_page(user=user, builder=builder)
    data_source = data_fixture.create_builder_local_baserow_list_rows_data_source(
        user=user,
        page=page,
        integration=integration,
        view=view,
        table=table,
    )

    url = reverse(
        "api:builder:data_source:dispatch", kwargs={"data_source_id": data_source.id}
    )

    advanced_filters = {
        "filter_type": "OR",
        "filters": [
            {
                "field": fields[0].id,
                "type": "equal",
                "value": "Peter",
            },
            {
                "field": fields[0].id,
                "type": "equal",
                "value": "Jérémie",
            },
        ],
    }

    response = api_client.post(
        f"{url}?filters={json.dumps(advanced_filters)}",
        {},
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )

    assert response.status_code == HTTP_200_OK
    assert response.json() == {
        "results": [
            {"id": 1, "order": AnyStr(), fields[0].db_column: "Peter"},
            {"id": 4, "order": AnyStr(), fields[0].db_column: "Jérémie"},
        ],
        "has_next_page": False,
    }


@pytest.mark.django_db
def test_dispatch_data_source_permission_denied(api_client, data_fixture):
    user, token = data_fixture.create_user_and_token()
    table, fields, rows = data_fixture.build_table(
        columns=[
            ("Name", "text"),
            ("My Color", "text"),
        ],
        rows=[
            ["BMW", "Blue"],
            ["Audi", "Orange"],
        ],
    )
    view = data_fixture.create_grid_view(user, table=table)
    builder = data_fixture.create_builder_application(user=user)
    integration = data_fixture.create_local_baserow_integration(
        user=user, application=builder
    )
    page = data_fixture.create_builder_page(user=user, builder=builder)
    data_source = data_fixture.create_builder_local_baserow_get_row_data_source(
        user=user,
        page=page,
        integration=integration,
        view=view,
        table=table,
        row_id="2",
    )

    url = reverse(
        "api:builder:data_source:dispatch", kwargs={"data_source_id": data_source.id}
    )

    response = api_client.post(
        url,
        {},
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )

    assert response.status_code == HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_dispatch_data_source_using_formula(api_client, data_fixture):
    user, token = data_fixture.create_user_and_token()
    table, fields, rows = data_fixture.build_table(
        user=user,
        columns=[
            ("Name", "text"),
            ("My Color", "text"),
        ],
        rows=[
            ["BMW", "Blue"],
            ["Audi", "Orange"],
        ],
    )
    view = data_fixture.create_grid_view(user, table=table)
    builder = data_fixture.create_builder_application(user=user)
    integration = data_fixture.create_local_baserow_integration(
        user=user, application=builder
    )
    page = data_fixture.create_builder_page(user=user, builder=builder)
    data_source = data_fixture.create_builder_local_baserow_get_row_data_source(
        user=user,
        page=page,
        integration=integration,
        view=view,
        table=table,
        row_id='get("page_parameter.id")',
    )

    url = reverse(
        "api:builder:data_source:dispatch", kwargs={"data_source_id": data_source.id}
    )

    response = api_client.post(
        url,
        {"page_parameter": {"id": 2}, "data_source": {"page_id": page.id}},
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )

    assert response.status_code == HTTP_200_OK
    assert response.json() == {
        "id": 2,
        "order": AnyStr(),
        fields[0].db_column: "Audi",
        fields[1].db_column: "Orange",
    }


@pytest.mark.django_db
def test_dispatch_data_source_improperly_configured(api_client, data_fixture):
    user, token = data_fixture.create_user_and_token()
    table, fields, rows = data_fixture.build_table(
        user=user,
        columns=[
            ("Name", "text"),
            ("My Color", "text"),
        ],
        rows=[
            ["BMW", "Blue"],
            ["Audi", "2"],
        ],
    )
    view = data_fixture.create_grid_view(user, table=table)
    builder = data_fixture.create_builder_application(user=user)
    integration = data_fixture.create_local_baserow_integration(
        user=user, application=builder
    )
    page = data_fixture.create_builder_page(user=user, builder=builder)
    data_source0 = data_fixture.create_builder_local_baserow_get_row_data_source(
        user=user,
        page=page,
        integration=integration,
        view=view,
        table=table,
        row_id="1",
        name="Working",
    )

    data_source1 = data_fixture.create_builder_local_baserow_get_row_data_source(
        user=user,
        page=page,
        integration=integration,
        row_id='get("page_parameter.id")',
    )
    data_source2 = data_fixture.create_builder_local_baserow_get_row_data_source(
        user=user,
        page=page,
        view=view,
        table=table,
        integration=None,
        row_id='get("page_parameter.id")',
    )
    data_source3 = data_fixture.create_builder_local_baserow_get_row_data_source(
        user=user,
        page=page,
        integration=integration,
        view=view,
        table=table,
        row_id='get("page_parameter.id")',
    )
    data_source4 = data_fixture.create_builder_local_baserow_get_row_data_source(
        user=user,
        page=page,
        integration=integration,
        view=view,
        table=table,
        row_id='get("data_source.Working.My Color")',
    )

    url = reverse(
        "api:builder:data_source:dispatch", kwargs={"data_source_id": data_source1.id}
    )

    # The given dispatch query context is wrong
    response = api_client.post(
        url,
        {
            "page_parameter": {"id": 2},
        },
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )

    assert response.status_code == HTTP_400_BAD_REQUEST
    assert response.json()["error"] == "ERROR_DATA_SOURCE_IMPROPERLY_CONFIGURED"
    assert (
        response.json()["detail"] == "The data_source configuration is incorrect: "
        "The table property is missing."
    )

    url = reverse(
        "api:builder:data_source:dispatch", kwargs={"data_source_id": data_source2.id}
    )

    # The given dispatch query context is wrong
    response = api_client.post(
        url,
        {
            "page_parameter": {"id": 2},
        },
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )

    assert response.status_code == HTTP_400_BAD_REQUEST
    assert response.json()["error"] == "ERROR_DATA_SOURCE_IMPROPERLY_CONFIGURED"
    assert (
        response.json()["detail"] == "The data_source configuration is incorrect: "
        "The integration property is missing."
    )

    url = reverse(
        "api:builder:data_source:dispatch", kwargs={"data_source_id": data_source3.id}
    )

    # The given dispatch query context is wrong
    response = api_client.post(
        url,
        {
            "page_parameter": {"id": "test"},
        },
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )

    assert response.status_code == HTTP_400_BAD_REQUEST
    assert response.json()["error"] == "ERROR_DATA_SOURCE_IMPROPERLY_CONFIGURED"
    assert (
        response.json()["detail"] == "The data_source configuration is incorrect: "
        "The result of the `row_id` formula must be an integer or "
        "convertible to an integer."
    )

    url = reverse(
        "api:builder:data_source:dispatch", kwargs={"data_source_id": data_source4.id}
    )


@pytest.mark.django_db
def test_dispatch_data_sources(api_client, data_fixture):
    user, token = data_fixture.create_user_and_token()
    table, fields, rows = data_fixture.build_table(
        user=user,
        columns=[
            ("Name", "text"),
            ("My Color", "text"),
        ],
        rows=[
            ["BMW", "Blue"],
            ["Audi", "Orange"],
            ["2Cv", "Green"],
            ["Tesla", "Dark"],
        ],
    )
    view = data_fixture.create_grid_view(user, table=table)
    builder = data_fixture.create_builder_application(user=user)
    integration = data_fixture.create_local_baserow_integration(
        user=user, application=builder
    )
    page = data_fixture.create_builder_page(user=user, builder=builder)
    data_source = data_fixture.create_builder_local_baserow_get_row_data_source(
        user=user,
        page=page,
        integration=integration,
        view=view,
        table=table,
        row_id="2",
    )
    data_source1 = data_fixture.create_builder_local_baserow_get_row_data_source(
        user=user,
        page=page,
        integration=integration,
        view=view,
        table=table,
        row_id="3",
    )
    data_source2 = data_fixture.create_builder_local_baserow_get_row_data_source(
        user=user,
        page=page,
        integration=integration,
        view=view,
        table=table,
        row_id="4",
    )
    data_source3 = data_fixture.create_builder_local_baserow_get_row_data_source(
        user=user,
        page=page,
        integration=integration,
        view=view,
        table=table,
        row_id="bad",
    )
    data_source4 = data_fixture.create_builder_local_baserow_get_row_data_source(
        user=user, integration=integration, view=view, table=table, row_id="4"
    )

    url = reverse("api:builder:data_source:dispatch-all", kwargs={"page_id": page.id})

    response = api_client.post(
        url,
        {},
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )

    assert response.status_code == HTTP_200_OK
    assert response.json() == {
        str(data_source.id): {
            fields[1].db_column: "Orange",
            fields[0].db_column: "Audi",
            "id": rows[1].id,
            "order": AnyStr(),
        },
        str(data_source1.id): {
            fields[1].db_column: "Green",
            fields[0].db_column: "2Cv",
            "id": rows[2].id,
            "order": AnyStr(),
        },
        str(data_source2.id): {
            fields[1].db_column: "Dark",
            fields[0].db_column: "Tesla",
            "id": rows[3].id,
            "order": AnyStr(),
        },
        str(data_source3.id): {
            "_error": "ERROR_DATA_SOURCE_IMPROPERLY_CONFIGURED",
            "detail": "The data_source configuration is incorrect: "
            "The `row_id` formula can't be resolved: "
            "Invalid syntax at line 1, col 3: mismatched input "
            "'the end of the formula' expecting '('",
        },
    }


@pytest.mark.django_db
def test_get_record_names(api_client, data_fixture):
    user, token = data_fixture.create_user_and_token()
    builder = data_fixture.create_builder_application(user=user)
    integration = data_fixture.create_local_baserow_integration(
        user=user, application=builder
    )

    # There must exist one database with a primary column for the record name
    table = data_fixture.create_database_table(user=user)
    data_fixture.create_text_field(name="Name", table=table, primary=True)

    model = table.get_model(attribute_names=True)
    rows = {
        str(model.objects.create(name="BMW").id): "BMW",
        str(model.objects.create(name="Audi").id): "Audi",
        str(model.objects.create(name="2Cv").id): "2Cv",
        str(model.objects.create(name="Tesla").id): "Tesla",
    }

    data_source = data_fixture.create_builder_local_baserow_list_rows_data_source(
        user=user,
        table=table,
        integration=integration,
    )

    view_name = "api:builder:data_source:record-names"
    base_url = reverse(view_name, kwargs={"data_source_id": data_source.id})

    # If no `row_ids` query param is passed then it should return an empty result
    url = f"{base_url}?record_ids="
    response = api_client.get(url, format="json", HTTP_AUTHORIZATION=f"JWT {token}")
    assert response.status_code == HTTP_200_OK
    assert response.json() == {}

    # If the row ids are present, then it should return a mapping with the record names
    url = f"{base_url}?record_ids={','.join(rows.keys())}"
    response = api_client.get(url, format="json", HTTP_AUTHORIZATION=f"JWT {token}")
    assert response.status_code == HTTP_200_OK
    assert response.json() == rows

    # If `row_ids` are invalid, then it should raise an error
    url = f"{base_url}?record_ids=INVALID_1,INVALID_2"
    response = api_client.get(url, format="json", HTTP_AUTHORIZATION=f"JWT {token}")
    assert response.status_code == HTTP_400_BAD_REQUEST
    assert response.json()["error"] == "ERROR_DATA_SOURCE_IMPROPERLY_CONFIGURED"

    # If the data source is not a list data source, it should raise an error
    non_list_data_source = (
        data_fixture.create_builder_local_baserow_get_row_data_source(
            user=user,
            table=table,
            integration=integration,
        )
    )
    base_url = reverse(view_name, kwargs={"data_source_id": non_list_data_source.id})
    url = f"{base_url}?record_ids={','.join(rows.keys())}"
    response = api_client.get(url, format="json", HTTP_AUTHORIZATION=f"JWT {token}")
    assert response.status_code == HTTP_400_BAD_REQUEST
    assert response.json()["error"] == "ERROR_DATA_SOURCE_IMPROPERLY_CONFIGURED"


@pytest.fixture
def data_source_fixture(data_fixture):
    """A fixture to help test the DispatchDataSourcesView view."""

    user, token = data_fixture.create_user_and_token()
    table, fields, rows = data_fixture.build_table(
        user=user,
        columns=[
            ("Name", "text"),
            ("Color", "text"),
        ],
        rows=[
            ["Apple", "Red"],
            ["Banana", "Yellow"],
            ["Cherry", "Purple"],
        ],
    )
    builder = data_fixture.create_builder_application(user=user)
    integration = data_fixture.create_local_baserow_integration(
        user=user, application=builder
    )
    page = data_fixture.create_builder_page(user=user, builder=builder)

    return {
        "user": user,
        "token": token,
        "page": page,
        "integration": integration,
        "table": table,
        "rows": rows,
        "fields": fields,
    }


@pytest.mark.django_db
def test_dispatch_data_sources_list_rows_no_elements(
    api_client, data_fixture, data_source_fixture
):
    """
    Test the DispatchDataSourcesView endpoint when using a Data Source type
    of List Rows.

    If the page has zero elements, the API response should not contain any
    field specific data.
    """

    data_source = data_fixture.create_builder_local_baserow_list_rows_data_source(
        user=data_source_fixture["user"],
        page=data_source_fixture["page"],
        integration=data_source_fixture["integration"],
        table=data_source_fixture["table"],
    )

    url = reverse(
        "api:builder:domains:public_dispatch_all",
        kwargs={"page_id": data_source_fixture["page"].id},
    )

    response = api_client.post(
        url,
        {},
        format="json",
        HTTP_AUTHORIZATION=f"JWT {data_source_fixture['token']}",
    )

    rows = data_source_fixture["rows"]
    assert response.status_code == HTTP_200_OK
    assert response.json() == {
        str(data_source.id): {
            "has_next_page": False,
            "results": [
                {
                    "id": rows[0].id,
                    "order": str(rows[0].order),
                },
                {
                    "id": rows[1].id,
                    "order": str(rows[1].order),
                },
                {
                    "id": rows[2].id,
                    "order": str(rows[2].order),
                },
            ],
        },
    }


@pytest.mark.django_db
def test_dispatch_data_sources_get_row_no_elements(
    api_client, data_fixture, data_source_fixture
):
    """
    Test the DispatchDataSourcesView endpoint when using a Data Source type
    of Get Row.

    If the page has zero elements, the API response should not contain any
    field specific data.
    """

    data_source = data_fixture.create_builder_local_baserow_get_row_data_source(
        user=data_source_fixture["user"],
        page=data_source_fixture["page"],
        integration=data_source_fixture["integration"],
        table=data_source_fixture["table"],
        row_id="2",
    )

    url = reverse(
        "api:builder:domains:public_dispatch_all",
        kwargs={"page_id": data_source_fixture["page"].id},
    )

    response = api_client.post(
        url,
        {},
        format="json",
        HTTP_AUTHORIZATION=f"JWT {data_source_fixture['token']}",
    )

    rows = data_source_fixture["rows"]
    assert response.status_code == HTTP_200_OK
    assert response.json() == {
        str(data_source.id): {
            "id": rows[1].id,
            "order": str(rows[1].order),
        }
    }


@pytest.mark.django_db
def test_dispatch_data_sources_list_rows_with_elements(
    api_client, data_fixture, data_source_fixture
):
    """
    Test the DispatchDataSourcesView endpoint when using a Data Source type
    of List Rows.

    The API response should only contain field data when the field is
    referenced in an element via a formula.
    """

    data_source = data_fixture.create_builder_local_baserow_list_rows_data_source(
        user=data_source_fixture["user"],
        page=data_source_fixture["page"],
        integration=data_source_fixture["integration"],
        table=data_source_fixture["table"],
    )

    field_id = data_source_fixture["fields"][0].id

    # Create an element that uses a formula referencing the data source
    data_fixture.create_builder_table_element(
        page=data_source_fixture["page"],
        data_source=data_source,
        fields=[
            {
                "name": "FieldA",
                "type": "text",
                "config": {"value": f"get('current_record.field_{field_id}')"},
            },
        ],
    )

    url = reverse(
        "api:builder:domains:public_dispatch_all",
        kwargs={"page_id": data_source_fixture["page"].id},
    )

    response = api_client.post(
        url,
        {},
        format="json",
        HTTP_AUTHORIZATION=f"JWT {data_source_fixture['token']}",
    )

    expected_results = []
    rows = data_source_fixture["rows"]
    for row in rows:
        expected_results.append(
            {
                f"field_{field_id}": getattr(row, f"field_{field_id}"),
                "id": row.id,
                "order": str(row.order),
            }
        )

    assert response.status_code == HTTP_200_OK
    # Although this Data Source has 2 Fields/Columns, only one is returned
    # since only one field_id is used by the Table.
    assert response.json() == {
        str(data_source.id): {
            "has_next_page": False,
            "results": expected_results,
        },
    }


@pytest.mark.django_db
@pytest.mark.parametrize(
    # table_row_id is 1-indexed to reflect the row ID in formulas
    # db_row_id is 0-indexed to reflect the row ID in the database
    "table_row_id,db_row_id,",
    [
        (1, 0),
        (2, 1),
        (3, 2),
    ],
)
def test_dispatch_data_sources_get_row_with_elements(
    api_client, data_fixture, data_source_fixture, table_row_id, db_row_id
):
    """
    Test the DispatchDataSourcesView endpoint when using a Data Source type
    of Get Row.

    The API response should only contain field data when the field is
    referenced in an element via a formula.
    """

    data_source = data_fixture.create_builder_local_baserow_get_row_data_source(
        user=data_source_fixture["user"],
        page=data_source_fixture["page"],
        integration=data_source_fixture["integration"],
        table=data_source_fixture["table"],
        row_id=table_row_id,
    )

    field_id = data_source_fixture["fields"][0].id

    # Create an element that uses a formula referencing the data source
    data_fixture.create_builder_table_element(
        page=data_source_fixture["page"],
        data_source=data_source,
        fields=[
            {
                "name": "FieldA",
                "type": "text",
                "config": {
                    "value": f"get('data_source.{data_source.id}.field_{field_id}')"
                },
            },
        ],
    )

    url = reverse(
        "api:builder:domains:public_dispatch_all",
        kwargs={"page_id": data_source_fixture["page"].id},
    )

    response = api_client.post(
        url,
        {},
        format="json",
        HTTP_AUTHORIZATION=f"JWT {data_source_fixture['token']}",
    )

    rows = data_source_fixture["rows"]
    assert response.status_code == HTTP_200_OK
    assert response.json() == {
        str(data_source.id): {
            f"field_{field_id}": getattr(rows[db_row_id], f"field_{field_id}"),
            "id": rows[db_row_id].id,
            "order": str(rows[db_row_id].order),
        }
    }


@pytest.mark.django_db
def test_dispatch_data_sources_get_and_list_rows_with_elements(
    api_client,
    data_fixture,
    data_source_fixture,
):
    """
    Test the DispatchDataSourcesView endpoint when using a mix of Data Source
    types, i.e. Get Row and List Rows.

    The API response should only contain field data when the field is
    referenced in an element via a formula.
    """

    user = data_source_fixture["user"]
    table_1, fields_1, rows_1 = data_fixture.build_table(
        user=user,
        columns=[
            ("Food", "text"),
        ],
        rows=[
            ["Palak Paneer", "Paneer Pakora"],
        ],
    )
    data_source_1 = data_fixture.create_builder_local_baserow_get_row_data_source(
        user=data_source_fixture["user"],
        page=data_source_fixture["page"],
        integration=data_source_fixture["integration"],
        table=table_1,
        row_id=1,
    )

    table_2, fields_2, rows_2 = data_fixture.build_table(
        user=user,
        columns=[
            ("Fruits", "text"),
        ],
        rows=[
            ["Kiwi", "Cherry"],
        ],
    )
    data_source_2 = data_fixture.create_builder_local_baserow_list_rows_data_source(
        user=user,
        page=data_source_fixture["page"],
        integration=data_source_fixture["integration"],
        table=table_2,
    )

    # Create an element that uses a concatenation of two "get" formulas; one
    # using the Get Row and the other using List Row data sources.
    formula = (
        f"concat(get('current_record.field_{fields_1[0].id}'),"
        f"get('data_source.{data_source_1.id}.field_{fields_1[0].id}'))"
    )
    data_fixture.create_builder_table_element(
        page=data_source_fixture["page"],
        data_source=data_source_1,
        fields=[
            {
                "name": "My Dishes",
                "type": "text",
                "config": {"value": formula},
            },
        ],
    )

    # Create another table, this time using the List Row data source
    data_fixture.create_builder_table_element(
        page=data_source_fixture["page"],
        data_source=data_source_2,
        fields=[
            {
                "name": "My Fruits",
                "type": "text",
                "config": {"value": f"get('current_record.field_{fields_2[0].id}')"},
            },
        ],
    )

    url = reverse(
        "api:builder:domains:public_dispatch_all",
        kwargs={"page_id": data_source_fixture["page"].id},
    )

    response = api_client.post(
        url,
        {},
        format="json",
        HTTP_AUTHORIZATION=f"JWT {data_source_fixture['token']}",
    )

    assert response.status_code == HTTP_200_OK
    assert response.json() == {
        str(data_source_1.id): {
            f"field_{fields_1[0].id}": getattr(rows_1[0], f"field_{fields_1[0].id}"),
            "id": rows_1[0].id,
            "order": str(rows_1[0].order),
        },
        # Although this Data Source has 2 Fields/Columns, only one is returned
        # since only one field_id is used by the Table.
        str(data_source_2.id): {
            "has_next_page": False,
            "results": [
                {
                    f"field_{fields_2[0].id}": getattr(
                        rows_2[0], f"field_{fields_2[0].id}"
                    ),
                    "id": rows_2[0].id,
                    "order": str(rows_2[0].order),
                },
            ],
        },
    }


@pytest.fixture
def data_source_element_roles_fixture(data_fixture):
    """
    A fixture to help test the DispatchDataSourcesView view using Elements
    and user roles.
    """

    user = data_fixture.create_user()
    builder = data_fixture.create_builder_application(user=user)
    builder_to = data_fixture.create_builder_application(workspace=None)
    data_fixture.create_builder_custom_domain(builder=builder, published_to=builder_to)
    public_page = data_fixture.create_builder_page(builder=builder_to)

    table, fields, rows = data_fixture.build_table(
        user=user,
        columns=[
            ("Name", "text"),
            ("Color", "text"),
        ],
        rows=[
            ["Apple", "Red"],
            ["Banana", "Yellow"],
            ["Cherry", "Purple"],
        ],
    )

    return {
        "page": public_page,
        "user": user,
        "table": table,
        "fields": fields,
        "rows": rows,
        "builder_to": builder_to,
    }


def create_user_table_and_role(data_fixture, user, builder, user_role):
    """Helper to create a User table with a particular user role."""

    # Create the user table for the user_source
    user_table, user_fields, user_rows = data_fixture.build_table(
        user=user,
        columns=[
            ("Email", "text"),
            ("Name", "text"),
            ("Password", "text"),
            ("Role", "text"),
        ],
        rows=[
            ["foo@bar.com", "Foo User", "secret", user_role],
        ],
    )
    email_field, name_field, password_field, role_field = user_fields

    integration = data_fixture.create_local_baserow_integration(
        user=user, application=builder
    )
    user_source = data_fixture.create_user_source(
        user_source_type_registry.get("local_baserow").model_class,
        application=builder,
        integration=integration,
        table=user_table,
        email_field=email_field,
        name_field=name_field,
        role_field=role_field,
    )

    return user_source, integration


@pytest.mark.django_db
@pytest.mark.parametrize(
    "user_role,element_role,expect_fields",
    [
        # When the user role doesn't match the Element's role,
        # the fields should *not* be returned.
        ("foo_role", "bar_role", False),
        # When the user and Element roles match, the fields should
        # be returned.
        ("foo_role", "foo_role", True),
    ],
)
def test_dispatch_data_sources_list_rows_with_elements_and_role(
    api_client,
    data_fixture,
    data_source_element_roles_fixture,
    user_role,
    element_role,
    expect_fields,
):
    """
    Test the DispatchDataSourcesView endpoint when using a Data Source type
    of List Rows.

    This test creates a Element with a role. Depending on whether expect_fields
    is True or False, the test checks to see if the Data Source view returns
    the fields.

    The API response should only contain field data when the field is
    referenced in an element via a formula, and that element is visible
    to the user.
    """

    page = data_source_element_roles_fixture["page"]

    user_source, integration = create_user_table_and_role(
        data_fixture,
        data_source_element_roles_fixture["user"],
        data_source_element_roles_fixture["builder_to"],
        user_role,
    )
    user_source_user = UserSourceUser(
        user_source, None, 1, "foo_username", "foo@bar.com"
    )
    token = user_source_user.get_refresh_token().access_token

    data_source = data_fixture.create_builder_local_baserow_list_rows_data_source(
        user=data_source_element_roles_fixture["user"],
        page=page,
        integration=integration,
        table=data_source_element_roles_fixture["table"],
    )

    field_id = data_source_element_roles_fixture["fields"][0].id

    # Create an element that uses a formula referencing the data source
    data_fixture.create_builder_table_element(
        page=page,
        data_source=data_source,
        visibility=Element.VISIBILITY_TYPES.LOGGED_IN,
        roles=[element_role],
        role_type=Element.ROLE_TYPES.DISALLOW_ALL_EXCEPT,
        fields=[
            {
                "name": "FieldA",
                "type": "text",
                "config": {"value": f"get('current_record.field_{field_id}')"},
            },
        ],
    )

    url = reverse(
        "api:builder:domains:public_dispatch_all",
        kwargs={"page_id": page.id},
    )

    response = api_client.post(
        url,
        {},
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )

    expected_results = []
    for row in data_source_element_roles_fixture["rows"]:
        result = {
            "id": row.id,
            "order": str(row.order),
        }
        if expect_fields:
            # Field should only be visible if the user's role allows them
            # to see the data source fields.
            result[f"field_{field_id}"] = getattr(row, f"field_{field_id}")

        expected_results.append(result)

    assert response.status_code == HTTP_200_OK
    assert response.json() == {
        str(data_source.id): {
            "has_next_page": False,
            "results": expected_results,
        },
    }


@pytest.mark.django_db
@patch(
    "baserow.contrib.builder.api.data_sources.views.DataSourceService.dispatch_data_source"
)
@patch("baserow.contrib.builder.api.data_sources.views.BuilderDispatchContext")
@patch(
    "baserow.contrib.builder.api.data_sources.views.DataSourceHandler.get_data_source"
)
def test_dispatch_data_source_view(
    mock_get_data_source,
    mock_builder_dispatch_context,
    mock_dispatch_data_source,
    api_client,
):
    """
    Test the DispatchDataSourceView endpoint.

    Ensure that the field_names are not computed, because we don't want to
    filter any fields in the Editor.
    """

    mock_data_source = MagicMock()
    mock_get_data_source.return_value = mock_data_source

    mock_dispatch_context = MagicMock()
    mock_builder_dispatch_context.return_value = mock_dispatch_context

    mock_response = {}
    mock_dispatch_data_source.return_value = mock_response

    mock_data_source_id = 100
    url = reverse(
        "api:builder:data_source:dispatch",
        kwargs={"data_source_id": mock_data_source_id},
    )
    response = api_client.post(url)

    assert response.status_code == 200
    assert response.json() == mock_response
    mock_get_data_source.assert_called_once_with(mock_data_source_id)
    mock_builder_dispatch_context.assert_called_once_with(
        ANY,
        mock_data_source.page,
        only_dispatch_formula_fields=False,
    )
    mock_dispatch_data_source.assert_called_once_with(
        ANY, mock_data_source, mock_dispatch_context
    )


@pytest.mark.django_db
@patch(
    "baserow.contrib.builder.api.data_sources.views.DataSourceService.dispatch_page_data_sources"
)
@patch("baserow.contrib.builder.api.data_sources.views.BuilderDispatchContext")
@patch("baserow.contrib.builder.api.data_sources.views.PageHandler.get_page")
def test_dispatch_data_sources_view(
    mock_get_page,
    mock_builder_dispatch_context,
    mock_dispatch_page_data_sources,
    api_client,
):
    """
    Test the DispatchDataSourcesView endpoint.

    Ensure that the field_names are not computed, because we don't want to
    filter any fields in the Editor.
    """

    mock_page = MagicMock()
    mock_get_page.return_value = mock_page

    mock_dispatch_context = MagicMock()
    mock_builder_dispatch_context.return_value = mock_dispatch_context

    mock_service_contents = {"101": "mock_content"}
    mock_dispatch_page_data_sources.return_value = mock_service_contents

    mock_page_id = 100
    url = reverse(
        "api:builder:data_source:dispatch-all", kwargs={"page_id": mock_page_id}
    )
    response = api_client.post(url)

    assert response.status_code == 200
    assert response.json() == mock_service_contents
    mock_get_page.assert_called_once_with(mock_page_id)
    mock_builder_dispatch_context.assert_called_once_with(
        ANY, mock_page, only_dispatch_formula_fields=False
    )
    mock_dispatch_page_data_sources.assert_called_once_with(
        ANY, mock_page, mock_dispatch_context
    )
