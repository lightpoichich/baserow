import json
import zipfile

from django.test.utils import override_settings
from django.urls import reverse

import pytest
from freezegun import freeze_time
from rest_framework.status import (
    HTTP_200_OK,
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


@pytest.mark.django_db(transaction=True)
def test_exporting_empty_workspace(
    data_fixture,
    api_client,
    tmpdir,
    settings,
    django_capture_on_commit_callbacks,
    use_tmp_media_root,
):
    user = data_fixture.create_user()
    workspace = data_fixture.create_workspace(user=user)

    run_time = "2024-10-14T08:00:00Z"
    with django_capture_on_commit_callbacks(execute=True), freeze_time(run_time):
        token = data_fixture.generate_token(user)
        response = api_client.post(
            reverse(
                "api:workspaces:export_workspace_async",
                kwargs={"workspace_id": workspace.id},
            ),
            data={
                "application_ids": [],
            },
            format="json",
            HTTP_AUTHORIZATION=f"JWT {token}",
        )
    response_json = response.json()

    job_id = response_json["id"]
    assert response_json == {
        "created_on": run_time,
        "exported_file_name": "",
        "human_readable_error": "",
        "id": job_id,
        "progress_percentage": 0,
        "state": "pending",
        "type": "export_applications",
        "url": None,
        "workspace_id": workspace.id,
    }

    token = data_fixture.generate_token(user)
    response = api_client.get(
        reverse("api:jobs:item", kwargs={"job_id": job_id}),
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )
    assert response.status_code == HTTP_200_OK
    response_json = response.json()

    file_name = response_json["exported_file_name"]

    assert response_json["state"] == "finished"
    assert response_json["progress_percentage"] == 100
    assert (
        response_json["url"] == f"http://localhost:8000/media/export_files/{file_name}"
    )

    file_path = tmpdir.join(settings.EXPORT_FILES_DIRECTORY, file_name)
    assert file_path.isfile()

    with zipfile.ZipFile(file_path, "r") as zip_ref:
        assert "data/workspace_export.json" in zip_ref.namelist()

        with zip_ref.open("data/workspace_export.json") as json_file:
            json_data = json.load(json_file)
            assert len(json_data) == 0


@pytest.mark.django_db(transaction=True)
def test_exporting_workspace_with_single_empty_database(
    data_fixture,
    api_client,
    tmpdir,
    settings,
    django_capture_on_commit_callbacks,
    use_tmp_media_root,
):
    user = data_fixture.create_user()
    database = data_fixture.create_database_application(user=user)

    run_time = "2024-10-14T08:00:00Z"
    with django_capture_on_commit_callbacks(execute=True), freeze_time(run_time):
        token = data_fixture.generate_token(user)
        response = api_client.post(
            reverse(
                "api:workspaces:export_workspace_async",
                kwargs={"workspace_id": database.workspace.id},
            ),
            data={
                "application_ids": [],
            },
            format="json",
            HTTP_AUTHORIZATION=f"JWT {token}",
        )
    response_json = response.json()

    job_id = response_json["id"]
    assert response_json == {
        "created_on": run_time,
        "exported_file_name": "",
        "human_readable_error": "",
        "id": job_id,
        "progress_percentage": 0,
        "state": "pending",
        "type": "export_applications",
        "url": None,
        "workspace_id": database.workspace.id,
    }

    token = data_fixture.generate_token(user)
    response = api_client.get(
        reverse("api:jobs:item", kwargs={"job_id": job_id}),
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )
    assert response.status_code == HTTP_200_OK
    response_json = response.json()

    file_name = response_json["exported_file_name"]

    assert response_json["state"] == "finished"
    assert response_json["progress_percentage"] == 100
    assert (
        response_json["url"] == f"http://localhost:8000/media/export_files/{file_name}"
    )

    file_path = tmpdir.join(settings.EXPORT_FILES_DIRECTORY, file_name)
    assert file_path.isfile()

    with zipfile.ZipFile(file_path, "r") as zip_ref:
        assert "data/workspace_export.json" in zip_ref.namelist()

        with zip_ref.open("data/workspace_export.json") as json_file:
            json_data = json.load(json_file)
            assert len(json_data) == 1
            assert json_data == [
                {
                    "id": database.id,
                    "name": database.name,
                    "order": database.order,
                    "type": "database",
                    "tables": [],
                }
            ]
