import json
import zipfile
from unittest.mock import patch

from django.core.files.storage import FileSystemStorage
from django.test.utils import override_settings
from django.urls import reverse

import pytest
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND

from baserow.contrib.database.rows.handler import RowHandler


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
            "api:database:export:export_workspace_async",
            kwargs={"workspace_id": workspace.id},
        ),
        data={},
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )
    assert response.status_code == HTTP_400_BAD_REQUEST
    assert response.json()["error"] == "ERROR_FEATURE_DISABLED"


@pytest.mark.django_db
def test_exporting_missing_workspace_returns_error(data_fixture, api_client, tmpdir):
    user, token = data_fixture.create_user_and_token()
    workspace = data_fixture.create_workspace(user=user)
    data_fixture.create_database_application(workspace=workspace)

    response = api_client.post(
        reverse(
            "api:database:export:export_workspace_async",
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
            "api:database:export:export_workspace_async",
            kwargs={"workspace_id": workspace.id},
        ),
        data={},
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token2}",
    )

    assert response.status_code == HTTP_400_BAD_REQUEST
    assert response.json()["error"] == "ERROR_USER_NOT_IN_GROUP"


@pytest.mark.django_db
def test_exporting_workspace_writes_file_to_storage(
    data_fixture, api_client, tmpdir, settings, django_capture_on_commit_callbacks
):
    user = data_fixture.create_user()
    table = data_fixture.create_database_table(user=user)
    text_field = data_fixture.create_text_field(table=table, name="text_field", order=0)

    row_handler = RowHandler()
    row_handler.create_row(
        user=user,
        table=table,
        values={
            text_field.id: "row #1",
        },
    )
    row_handler.create_row(
        user=user,
        table=table,
        values={
            text_field.id: "row #2",
        },
    )
    storage = FileSystemStorage(location=(str(tmpdir)), base_url="http://localhost")

    with patch("baserow.contrib.database.export.handler.default_storage", new=storage):
        token = data_fixture.generate_token(user)
        with django_capture_on_commit_callbacks(execute=True):
            response = api_client.post(
                reverse(
                    "api:database:export:export_workspace_async",
                    kwargs={"workspace_id": table.database.workspace.id},
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
            "exported_file_name": "",
            "human_readable_error": "",
            "id": job_id,
            "progress_percentage": 0,
            "state": "pending",
            "type": "export_applications",
            "url": None,
        }

        response = api_client.get(
            reverse("api:jobs:item", kwargs={"job_id": job_id}),
            format="json",
            HTTP_AUTHORIZATION=f"JWT {token}",
        )
        response_json = response.json()

        filename = response_json["exported_file_name"]

        assert response_json["state"] == "finished"
        assert response_json["progress_percentage"] == 100
        assert (
            response_json["url"]
            == f"{settings.PUBLIC_BACKEND_URL}/media/export_files/{filename}"
        )

        file_path = tmpdir.join(settings.EXPORT_FILES_DIRECTORY, filename)
        assert file_path.isfile()

        with zipfile.ZipFile(file_path, "r") as zip_ref:
            assert "data/workspace_export.json" in zip_ref.namelist()

            with zip_ref.open("data/workspace_export.json") as json_file:
                json_data = json.load(json_file)
                assert len(json_data) == 1
                assert json_data[0]["name"] == table.database.name

                assert len(json_data[0]["tables"]) == 1
                table = json_data[0]["tables"][0]
                assert len(table["fields"]) == 1
                assert table["fields"][0]["name"] == text_field.name
                assert len(table["rows"]) == 2
                assert table["rows"][0][f"field_{text_field.id}"] == "row #1"
                assert table["rows"][1][f"field_{text_field.id}"] == "row #2"
