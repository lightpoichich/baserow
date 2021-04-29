import pytest
from django.utils import timezone
from django.utils.datetime_safe import datetime

from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
)

from django.shortcuts import reverse

from baserow.core.models import (
    GROUP_USER_PERMISSION_MEMBER,
    GROUP_USER_PERMISSION_ADMIN,
)


@pytest.mark.django_db
def test_non_admin_cannot_see_admin_users_endpoint(api_client, data_fixture):
    non_staff_user, token = data_fixture.create_user_and_token(
        email="test@test.nl", password="password", first_name="Test1", is_staff=False
    )
    response = api_client.get(
        reverse("api:premium:admin_user:users"),
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )
    assert response.status_code == HTTP_401_UNAUTHORIZED
    assert response.json()["error"] == "ERROR_ADMIN_ONLY_OPERATION"


@pytest.mark.django_db
def test_admin_can_see_admin_users_endpoint(api_client, data_fixture):
    staff_user, token = data_fixture.create_user_and_token(
        email="test@test.nl",
        password="password",
        first_name="Test1",
        is_staff=True,
        date_joined=datetime(2021, 4, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
    )
    group_user_is_admin_of = data_fixture.create_group()
    data_fixture.create_user_group(
        group=group_user_is_admin_of,
        user=staff_user,
        permissions=GROUP_USER_PERMISSION_ADMIN,
    )
    group_user_is_not_admin_of = data_fixture.create_group()
    data_fixture.create_user_group(
        group=group_user_is_not_admin_of,
        user=staff_user,
        permissions=GROUP_USER_PERMISSION_MEMBER,
    )
    response = api_client.get(
        reverse("api:premium:admin_user:users"),
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )
    assert response.status_code == HTTP_200_OK
    assert response.json() == {
        "count": 1,
        "next": None,
        "previous": None,
        "results": [
            {
                "date_joined": "2021-04-01T01:00:00Z",
                "full_name": staff_user.first_name,
                "username": staff_user.email,
                "groups": [
                    {
                        "id": group_user_is_admin_of.id,
                        "name": group_user_is_admin_of.name,
                        "permissions": GROUP_USER_PERMISSION_ADMIN,
                    },
                    {
                        "id": group_user_is_not_admin_of.id,
                        "name": group_user_is_not_admin_of.name,
                        "permissions": GROUP_USER_PERMISSION_MEMBER,
                    },
                ],
                "id": staff_user.id,
                "is_staff": True,
                "is_active": True,
                "last_login": None,
            }
        ],
    }


@pytest.mark.django_db
def test_admin_with_invalid_token_cannot_see_admin_users(api_client, data_fixture):
    data_fixture.create_user_and_token(
        email="test@test.nl",
        password="password",
        first_name="Test1",
        is_staff=True,
    )
    response = api_client.get(
        reverse("api:premium:admin_user:users"),
        format="json",
        HTTP_AUTHORIZATION=f"JWT abc123",
    )
    assert response.status_code == HTTP_401_UNAUTHORIZED
    assert response.json()["error"] == "ERROR_DECODING_SIGNATURE"


@pytest.mark.django_db
def test_admin_accessing_invalid_user_admin_page_returns_error(
    api_client, data_fixture
):
    _, token = data_fixture.create_user_and_token(
        email="test@test.nl",
        password="password",
        first_name="Test1",
        is_staff=True,
    )
    url = reverse("api:premium:admin_user:users")
    response = api_client.get(
        f"{url}?page=2",
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )
    assert response.status_code == HTTP_400_BAD_REQUEST
    assert response.json()["error"] == "ERROR_INVALID_PAGE"


@pytest.mark.django_db
def test_admin_accessing_user_admin_with_invalid_page_size_returns_error(
    api_client, data_fixture
):
    _, token = data_fixture.create_user_and_token(
        email="test@test.nl",
        password="password",
        first_name="Test1",
        is_staff=True,
    )
    url = reverse("api:premium:admin_user:users")
    response = api_client.get(
        f"{url}?page=1&size=201",
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )
    assert response.status_code == HTTP_400_BAD_REQUEST
    assert response.json()["error"] == "ERROR_PAGE_SIZE_LIMIT"


@pytest.mark.django_db
def test_admin_can_search_users(api_client, data_fixture):
    _, token = data_fixture.create_user_and_token(
        email="test@test.nl",
        password="password",
        first_name="Test1",
        is_staff=True,
    )
    searched_for_user = data_fixture.create_user(
        email="specific_user@test.nl",
        password="password",
        first_name="Test1",
        date_joined=datetime(2021, 4, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
    )
    url = reverse("api:premium:admin_user:users")
    response = api_client.get(
        f"{url}?page=1&search=specific_user",
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )
    assert response.status_code == HTTP_200_OK
    assert response.json() == {
        "count": 1,
        "next": None,
        "previous": None,
        "results": [
            {
                "date_joined": "2021-04-01T01:00:00Z",
                "full_name": searched_for_user.first_name,
                "username": searched_for_user.email,
                "groups": [],
                "id": searched_for_user.id,
                "is_staff": False,
                "is_active": True,
                "last_login": None,
            }
        ],
    }


@pytest.mark.django_db
def test_admin_can_sort_users(api_client, data_fixture):
    _, token = data_fixture.create_user_and_token(
        email="test@test.nl",
        password="password",
        first_name="Test1",
        is_staff=True,
    )
    searched_for_user = data_fixture.create_user(
        email="specific_user@test.nl",
        password="password",
        first_name="Test1",
        date_joined=datetime(2021, 4, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
    )
    url = reverse("api:premium:admin_user:users")
    response = api_client.get(
        f"{url}?page=1&search=specific_user",
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )
    assert response.status_code == HTTP_200_OK
    assert response.json() == {
        "count": 1,
        "next": None,
        "previous": None,
        "results": [
            {
                "date_joined": "2021-04-01T01:00:00Z",
                "full_name": searched_for_user.first_name,
                "username": searched_for_user.email,
                "groups": [],
                "id": searched_for_user.id,
                "is_staff": False,
                "is_active": True,
                "last_login": None,
            }
        ],
    }


@pytest.mark.django_db
def test_throws_error_if_invalid_sort_field_provided(api_client, data_fixture):
    _, token = data_fixture.create_user_and_token(
        email="test@test.nl",
        password="password",
        first_name="Test1",
        is_staff=True,
    )
    url = reverse("api:premium:admin_user:users")
    response = api_client.get(
        f"{url}?page=1&sorts=-invalid_field_name",
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )
    assert response.status_code == HTTP_400_BAD_REQUEST
    assert response.json()["error"] == "INVALID_USER_ADMIN_SORT_ATTRIBUTE"


@pytest.mark.django_db
def test_throws_error_if_sort_direction_not_provided(api_client, data_fixture):
    _, token = data_fixture.create_user_and_token(
        email="test@test.nl",
        password="password",
        first_name="Test1",
        is_staff=True,
    )
    url = reverse("api:premium:admin_user:users")
    response = api_client.get(
        f"{url}?page=1&sorts=username",
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )
    assert response.status_code == HTTP_400_BAD_REQUEST
    assert response.json()["error"] == "INVALID_USER_ADMIN_SORT_DIRECTION"


@pytest.mark.django_db
def test_throws_error_if_invalid_sort_direction_provided(api_client, data_fixture):
    _, token = data_fixture.create_user_and_token(
        email="test@test.nl",
        password="password",
        first_name="Test1",
        is_staff=True,
    )
    url = reverse("api:premium:admin_user:users")
    response = api_client.get(
        f"{url}?page=1&sorts=*username",
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )
    assert response.status_code == HTTP_400_BAD_REQUEST
    assert response.json()["error"] == "INVALID_USER_ADMIN_SORT_DIRECTION"


@pytest.mark.django_db
def test_throws_error_if_invalid_sorts_mixed_with_valid_ones(api_client, data_fixture):
    _, token = data_fixture.create_user_and_token(
        email="test@test.nl",
        password="password",
        first_name="Test1",
        is_staff=True,
    )
    url = reverse("api:premium:admin_user:users")
    response = api_client.get(
        f"{url}?page=1&sorts=+username,username,-invalid_field",
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )
    assert response.status_code == HTTP_400_BAD_REQUEST
    assert response.json()["error"] == "INVALID_USER_ADMIN_SORT_DIRECTION"


@pytest.mark.django_db
def test_throws_error_if_blank_sorts_provided(api_client, data_fixture):
    _, token = data_fixture.create_user_and_token(
        email="test@test.nl",
        password="password",
        first_name="Test1",
        is_staff=True,
    )
    url = reverse("api:premium:admin_user:users")
    response = api_client.get(
        f"{url}?page=1&sorts=,,",
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )
    assert response.status_code == HTTP_400_BAD_REQUEST
    assert response.json()["error"] == "INVALID_USER_ADMIN_SORT_ATTRIBUTE"


@pytest.mark.django_db
def test_throws_error_if_no_sorts_provided(api_client, data_fixture):
    _, token = data_fixture.create_user_and_token(
        email="test@test.nl",
        password="password",
        first_name="Test1",
        is_staff=True,
    )
    url = reverse("api:premium:admin_user:users")
    response = api_client.get(
        f"{url}?page=1&sorts=",
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )
    assert response.status_code == HTTP_400_BAD_REQUEST
    assert response.json()["error"] == "INVALID_USER_ADMIN_SORT_ATTRIBUTE"


@pytest.mark.django_db
def test_non_admin_cannot_delete_user(api_client, data_fixture):
    _, non_admin_token = data_fixture.create_user_and_token(
        email="test@test.nl",
        password="password",
        first_name="Test1",
        is_staff=False,
    )
    user_to_delete = data_fixture.create_user(
        email="specific_user@test.nl",
        password="password",
        first_name="Test1",
    )
    url = reverse(
        "api:premium:admin_user:user_edit", kwargs={"user_id": user_to_delete.id}
    )
    response = api_client.delete(
        url,
        format="json",
        HTTP_AUTHORIZATION=f"JWT {non_admin_token}",
    )
    assert response.status_code == HTTP_401_UNAUTHORIZED
    assert response.json()["error"] == "ERROR_ADMIN_ONLY_OPERATION"


@pytest.mark.django_db
def test_admin_can_delete_user(api_client, data_fixture):
    _, token = data_fixture.create_user_and_token(
        email="test@test.nl",
        password="password",
        first_name="Test1",
        is_staff=True,
    )
    user_to_delete = data_fixture.create_user(
        email="specific_user@test.nl",
        password="password",
        first_name="Test1",
    )
    url = reverse(
        "api:premium:admin_user:user_edit", kwargs={"user_id": user_to_delete.id}
    )
    response = api_client.delete(
        url,
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )
    assert response.status_code == HTTP_200_OK

    response = api_client.get(
        reverse("api:premium:admin_user:users"),
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )
    assert response.status_code == HTTP_200_OK
    assert response.json()["count"] == 1


@pytest.mark.django_db
def test_non_admin_cannot_patch_user(api_client, data_fixture):
    non_admin_user, non_admin_user_token = data_fixture.create_user_and_token(
        email="test@test.nl",
        password="password",
        first_name="Test1",
        is_staff=False,
    )
    url = reverse(
        "api:premium:admin_user:user_edit", kwargs={"user_id": non_admin_user.id}
    )
    response = api_client.patch(
        url,
        {"username": "some_other_email@test.nl"},
        format="json",
        HTTP_AUTHORIZATION=f"JWT {non_admin_user_token}",
    )
    assert response.status_code == HTTP_401_UNAUTHORIZED
    assert response.json()["error"] == "ERROR_ADMIN_ONLY_OPERATION"

    non_admin_user.refresh_from_db()
    assert non_admin_user.email == "test@test.nl"


@pytest.mark.django_db
def test_admin_can_patch_user(api_client, data_fixture):
    user, token = data_fixture.create_user_and_token(
        email="test@test.nl",
        password="password",
        first_name="Test1",
        is_staff=True,
        date_joined=datetime(2021, 4, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
    )
    url = reverse("api:premium:admin_user:user_edit", kwargs={"user_id": user.id})
    old_password = user.password
    response = api_client.patch(
        url,
        {"username": "some_other_email@test.nl", "password": "new_password"},
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )
    user.refresh_from_db()
    assert user.password != old_password
    assert response.status_code == HTTP_200_OK
    assert response.json() == {
        "date_joined": "2021-04-01T01:00:00Z",
        "full_name": user.first_name,
        "username": "some_other_email@test.nl",
        "groups": [],
        "id": user.id,
        "is_staff": True,
        "is_active": True,
        "last_login": None,
    }


@pytest.mark.django_db
def test_error_returned_when_invalid_field_supplied_to_edit(api_client, data_fixture):
    user, token = data_fixture.create_user_and_token(
        email="test@test.nl",
        password="password",
        first_name="Test1",
        is_staff=True,
        date_joined=datetime(2021, 4, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
    )
    url = reverse("api:premium:admin_user:user_edit", kwargs={"user_id": user.id})
    response = api_client.patch(
        url,
        {"date_joined": "2021-04-01T01:00:00Z"},
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )
    assert response.status_code == HTTP_400_BAD_REQUEST
    assert response.json()["error"] == "INVALID_USER_ADMIN_UPDATE"
