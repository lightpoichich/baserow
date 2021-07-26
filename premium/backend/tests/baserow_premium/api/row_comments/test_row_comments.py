import pytest
from freezegun import freeze_time
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK


@pytest.mark.django_db
def test_row_comments(data_fixture, api_client):
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
