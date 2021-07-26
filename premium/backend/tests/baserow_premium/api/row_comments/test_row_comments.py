import pytest
from django.conf import settings
from freezegun import freeze_time
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_row_comments_api_view(data_fixture, api_client):
    user, token = data_fixture.create_user_and_token(first_name="Test User")
    table, fields, rows = data_fixture.build_table(
        columns=[("text", "text")], rows=["first row", "second_row"], user=user
    )

    response = api_client.get(
        reverse(
            "api:premium:row_comments:item",
            kwargs={"table_id": table.id, "row_id": rows[0].id},
        ),
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )
    assert response.status_code == HTTP_200_OK
    assert response.json() == []

    with freeze_time("2020-01-01 12:00"):
        response = api_client.post(
            reverse(
                "api:premium:row_comments:item",
                kwargs={"table_id": table.id, "row_id": rows[0].id},
            ),
            {"comment": "My test comment"},
            format="json",
            HTTP_AUTHORIZATION=f"JWT {token}",
        )
    assert response.status_code == HTTP_200_OK
    expected_comment_json = {
        "comment": "My test comment",
        "created_on": "2020-01-01T12:00:00Z",
        "first_name": "Test User",
        "id": 1,
        "row_id": rows[0].id,
        "table": table.id,
        "updated_on": "2020-01-01T12:00:00Z",
        "user": user.id,
    }
    assert response.json() == expected_comment_json

    response = api_client.get(
        reverse(
            "api:premium:row_comments:item",
            kwargs={"table_id": table.id, "row_id": rows[0].id},
        ),
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )
    assert response.status_code == HTTP_200_OK
    assert response.json() == [expected_comment_json]


@pytest.mark.django_db
def test_row_comments_cant_view_comments_for_invalid_table(data_fixture, api_client):
    user, token = data_fixture.create_user_and_token(first_name="Test User")

    response = api_client.get(
        reverse(
            "api:premium:row_comments:item",
            kwargs={"table_id": 9999, "row_id": 0},
        ),
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )
    assert response.status_code == HTTP_404_NOT_FOUND
    assert response.json()["error"] == "ERROR_TABLE_DOES_NOT_EXIST"


@pytest.mark.django_db
def test_row_comments_cant_view_comments_for_invalid_row_in_table(
    data_fixture, api_client
):
    user, token = data_fixture.create_user_and_token(first_name="Test User")
    table, fields, rows = data_fixture.build_table(
        columns=[("text", "text")], rows=["first row"], user=user
    )

    response = api_client.get(
        reverse(
            "api:premium:row_comments:item",
            kwargs={"table_id": table.id, "row_id": 9999},
        ),
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )
    assert response.status_code == HTTP_404_NOT_FOUND
    assert response.json()["error"] == "ERROR_ROW_DOES_NOT_EXIST"


@pytest.mark.django_db
def test_row_comments_users_cant_view_comments_for_table_they_are_not_in_group_for(
    data_fixture, api_client
):
    user, token = data_fixture.create_user_and_token(first_name="Test User")
    other_user, other_token = data_fixture.create_user_and_token(first_name="Test User")
    table, fields, rows = data_fixture.build_table(
        columns=[("text", "text")], rows=["first row"], user=user
    )

    response = api_client.get(
        reverse(
            "api:premium:row_comments:item",
            kwargs={"table_id": table.id, "row_id": rows[0].id},
        ),
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )
    assert response.status_code == HTTP_200_OK

    response = api_client.get(
        reverse(
            "api:premium:row_comments:item",
            kwargs={"table_id": table.id, "row_id": rows[0].id},
        ),
        format="json",
        HTTP_AUTHORIZATION=f"JWT {other_token}",
    )
    assert response.json()["error"] == "ERROR_USER_NOT_IN_GROUP"
    assert response.status_code == HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_row_comments_cant_create_comments_in_invalid_table(data_fixture, api_client):
    user, token = data_fixture.create_user_and_token(first_name="Test User")

    response = api_client.post(
        reverse(
            "api:premium:row_comments:item",
            kwargs={"table_id": 9999, "row_id": 0},
        ),
        {"comment": "Test"},
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )
    assert response.status_code == HTTP_404_NOT_FOUND
    assert response.json()["error"] == "ERROR_TABLE_DOES_NOT_EXIST"


@pytest.mark.django_db
def test_row_comments_cant_create_comments_in_invalid_row_in_table(
    data_fixture, api_client
):
    user, token = data_fixture.create_user_and_token(first_name="Test User")
    table, fields, rows = data_fixture.build_table(
        columns=[("text", "text")], rows=["first row"], user=user
    )

    response = api_client.post(
        reverse(
            "api:premium:row_comments:item",
            kwargs={"table_id": table.id, "row_id": 9999},
        ),
        {"comment": "Test"},
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )
    assert response.status_code == HTTP_404_NOT_FOUND
    assert response.json()["error"] == "ERROR_ROW_DOES_NOT_EXIST"


@pytest.mark.django_db
def test_row_comments_users_cant_create_comments_for_table_they_are_not_in_group_for(
    data_fixture, api_client
):
    user, token = data_fixture.create_user_and_token(first_name="Test User")
    other_user, other_token = data_fixture.create_user_and_token(first_name="Test User")
    table, fields, rows = data_fixture.build_table(
        columns=[("text", "text")], rows=["first row"], user=user
    )

    response = api_client.post(
        reverse(
            "api:premium:row_comments:item",
            kwargs={"table_id": table.id, "row_id": rows[0].id},
        ),
        {"comment": "Test"},
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )
    assert response.status_code == HTTP_200_OK

    response = api_client.post(
        reverse(
            "api:premium:row_comments:item",
            kwargs={"table_id": table.id, "row_id": rows[0].id},
        ),
        {"comment": "Test"},
        format="json",
        HTTP_AUTHORIZATION=f"JWT {other_token}",
    )
    assert response.json()["error"] == "ERROR_USER_NOT_IN_GROUP"
    assert response.status_code == HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_cant_make_a_blank_row_comment(data_fixture, api_client):
    user, token = data_fixture.create_user_and_token(first_name="Test User")
    table, fields, rows = data_fixture.build_table(
        columns=[("text", "text")], rows=["first row"], user=user
    )

    response = api_client.post(
        reverse(
            "api:premium:row_comments:item",
            kwargs={"table_id": table.id, "row_id": rows[0].id},
        ),
        {"comment": ""},
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )
    assert response.status_code == HTTP_400_BAD_REQUEST
    assert response.json()["error"] == "ERROR_REQUEST_BODY_VALIDATION"
    assert response.json()["detail"] == {
        "comment": [{"code": "blank", "error": "This field may not be blank."}]
    }


@pytest.mark.django_db
def test_cant_make_a_row_comment_greater_than_max_settings(data_fixture, api_client):
    user, token = data_fixture.create_user_and_token(first_name="Test User")
    table, fields, rows = data_fixture.build_table(
        columns=[("text", "text")], rows=["first row"], user=user
    )
    response = api_client.post(
        reverse(
            "api:premium:row_comments:item",
            kwargs={"table_id": table.id, "row_id": rows[0].id},
        ),
        {"comment": "1" * settings.MAX_ROW_COMMENT_LENGTH},
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )
    assert response.status_code == HTTP_200_OK

    response = api_client.post(
        reverse(
            "api:premium:row_comments:item",
            kwargs={"table_id": table.id, "row_id": rows[0].id},
        ),
        {"comment": "1" * (settings.MAX_ROW_COMMENT_LENGTH + 1)},
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )
    assert response.status_code == HTTP_400_BAD_REQUEST
    assert response.json()["error"] == "ERROR_REQUEST_BODY_VALIDATION"
    assert response.json()["detail"] == {
        "comment": [
            {
                "code": "max_length",
                "error": f"Ensure this field has no more than "
                f"{settings.MAX_ROW_COMMENT_LENGTH} characters.",
            }
        ]
    }
