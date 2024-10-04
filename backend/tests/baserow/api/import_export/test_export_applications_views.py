from django.test.utils import override_settings
from django.urls import reverse

import pytest
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
)


@pytest.mark.django_db
@override_settings(
    FEATURE_FLAGS="",
)
def test_exporting_workspace_with_feature_flag_disabled(
    data_fixture, api_client, tmpdir
):
    user, token = data_fixture.create_user_and_token()
    workspace = data_fixture.create_workspace(user=user)
    data_fixture.create_database_application(workspace=workspace)

    response = api_client.post(
        reverse(
            "api:workspaces:export_workspace_async",
            kwargs={"workspace_id": workspace.id},
        ),
        data={},
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )
    assert response.status_code == HTTP_403_FORBIDDEN
    assert response.json()["error"] == "ERROR_FEATURE_DISABLED"


@pytest.mark.django_db
def test_exporting_missing_workspace_returns_error(data_fixture, api_client, tmpdir):
    user, token = data_fixture.create_user_and_token()
    workspace = data_fixture.create_workspace(user=user)
    data_fixture.create_database_application(workspace=workspace)

    response = api_client.post(
        reverse(
            "api:workspaces:export_workspace_async",
            kwargs={"workspace_id": 9999},
        ),
        data={},
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )

    assert response.status_code == HTTP_404_NOT_FOUND
    assert response.json()["error"] == "ERROR_GROUP_DOES_NOT_EXIST"


@pytest.mark.django_db
def test_exporting_workspace_with_no_permissions_returns_error(
    data_fixture, api_client, tmpdir
):
    user, token = data_fixture.create_user_and_token()
    _, token2 = data_fixture.create_user_and_token()
    workspace = data_fixture.create_workspace(user=user)
    data_fixture.create_database_application(workspace=workspace)

    response = api_client.post(
        reverse(
            "api:workspaces:export_workspace_async",
            kwargs={"workspace_id": workspace.id},
        ),
        data={},
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token2}",
    )

    assert response.status_code == HTTP_400_BAD_REQUEST
    assert response.json()["error"] == "ERROR_USER_NOT_IN_GROUP"


@pytest.mark.django_db
def test_exporting_workspace_with_application_without_permissions_returns_error(
    data_fixture, api_client, tmpdir
):
    user, token = data_fixture.create_user_and_token()
    workspace = data_fixture.create_workspace(user=user)
    database = data_fixture.create_database_application(workspace=workspace)

    user2, token2 = data_fixture.create_user_and_token()
    workspace2 = data_fixture.create_workspace(user=user2)
    database2 = data_fixture.create_database_application(workspace=workspace2)

    response = api_client.post(
        reverse(
            "api:workspaces:export_workspace_async",
            kwargs={"workspace_id": workspace.id},
        ),
        data={"application_ids": [database.id, database2.id]},
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )

    assert response.status_code == HTTP_401_UNAUTHORIZED
    assert response.json()["error"] == "PERMISSION_DENIED"
