from unittest.mock import patch

import pytest
from django.core.files.storage import FileSystemStorage
from django.urls import reverse
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from django.utils.timezone import utc, make_aware
from django_capture_on_commit_callbacks import capture_on_commit_callbacks
from freezegun import freeze_time
from rest_framework.fields import DateTimeField

from baserow.contrib.database.rows.handler import RowHandler


@pytest.mark.django_db
def test_exporting_json_writes_file_to_storage(
    data_fixture, api_client, tmpdir, settings
):
    user, token = data_fixture.create_user_and_token()
    table = data_fixture.create_database_table(user=user)
    text_field = data_fixture.create_text_field(table=table, name="text_field", order=0)
    option_field = data_fixture.create_single_select_field(
        table=table, name="option_field", order=1
    )
    option_a = data_fixture.create_select_option(
        field=option_field, value="A", color="blue"
    )
    option_b = data_fixture.create_select_option(
        field=option_field, value="B", color="red"
    )
    date_field = data_fixture.create_date_field(
        table=table,
        date_include_time=True,
        date_format="US",
        name="date_field",
        order=2,
    )

    grid_view = data_fixture.create_grid_view(table=table)
    data_fixture.create_view_filter(
        view=grid_view, field=text_field, type="contains", value="test"
    )
    data_fixture.create_view_sort(view=grid_view, field=text_field, order="ASC")

    row_handler = RowHandler()
    row_handler.create_row(
        user=user,
        table=table,
        values={
            text_field.id: "test",
            date_field.id: "2020-02-01 01:23",
            option_field.id: option_b.id,
        },
    )
    row_handler.create_row(
        user=user,
        table=table,
        values={
            text_field.id: "atest",
            date_field.id: "2020-02-01 01:23",
            option_field.id: option_a.id,
        },
    )
    storage = FileSystemStorage(location=(str(tmpdir)), base_url="http://localhost")

    with patch("baserow.contrib.database.export.handler.default_storage", new=storage):
        run_time = make_aware(parse_datetime("2020-02-01 01:00"), timezone=utc)
        # DRF uses some custom internal date time formatting, use the field itself
        # so the test doesn't break if we set a different default timezone format etc
        expected_expiry_time = DateTimeField().to_representation(
            run_time + timezone.timedelta(minutes=settings.EXPORT_FILE_EXPIRE_MINUTES)
        )
        with freeze_time(run_time):
            with capture_on_commit_callbacks(execute=True):
                response = api_client.post(
                    reverse(
                        "api:database:export:export_view",
                        kwargs={"view_id": grid_view.id},
                    ),
                    data={
                        "exporter_type": "json",
                        "json_charset": "utf-8",
                    },
                    format="json",
                    HTTP_AUTHORIZATION=f"JWT {token}",
                )
            response_json = response.json()
            assert "id" in response_json
            job_id = response_json["id"]
            assert response_json == {
                "id": job_id,
                "expires_at": expected_expiry_time,
                "exported_file_name": None,
                "exporter_type": "json",
                "progress_percentage": 0.0,
                "status": "pending",
                "table": table.id,
                "view": grid_view.id,
                "url": None,
            }
            response = api_client.get(
                reverse("api:database:export:get", kwargs={"job_id": job_id}),
                format="json",
                HTTP_AUTHORIZATION=f"JWT {token}",
            )
            response_json = response.json()
            assert "exported_file_name" in response_json
            filename = response_json["exported_file_name"]
            assert response_json == {
                "id": job_id,
                "expires_at": expected_expiry_time,
                "exported_file_name": filename,
                "exporter_type": "json",
                "progress_percentage": 1.0,
                "status": "complete",
                "table": table.id,
                "view": grid_view.id,
                "url": f"http://localhost:8000/media/export_files/{filename}",
            }

            file_path = tmpdir.join(settings.EXPORT_FILES_DIRECTORY, filename)
            assert file_path.isfile()
            expected = """[
{
    "id": 2,
    "text_field": "atest",
    "option_field": "A",
    "date_field": "02/01/2020 01:23"
},
{
    "id": 1,
    "text_field": "test",
    "option_field": "B",
    "date_field": "02/01/2020 01:23"
}
]
"""
            with open(file_path, "r", encoding="utf-8") as written_file:
                real = written_file.read()
                assert real == expected


@pytest.mark.django_db
def test_exporting_xml_writes_file_to_storage(
    data_fixture, api_client, tmpdir, settings
):
    user, token = data_fixture.create_user_and_token()
    table = data_fixture.create_database_table(user=user)
    text_field = data_fixture.create_text_field(table=table, name="text_field", order=0)
    option_field = data_fixture.create_single_select_field(
        table=table, name="option_field", order=1
    )
    option_a = data_fixture.create_select_option(
        field=option_field, value="A", color="blue"
    )
    option_b = data_fixture.create_select_option(
        field=option_field, value="B", color="red"
    )
    date_field = data_fixture.create_date_field(
        table=table,
        date_include_time=True,
        date_format="US",
        name="date_field",
        order=2,
    )

    grid_view = data_fixture.create_grid_view(table=table)
    data_fixture.create_view_filter(
        view=grid_view, field=text_field, type="contains", value="test"
    )
    data_fixture.create_view_sort(view=grid_view, field=text_field, order="ASC")

    row_handler = RowHandler()
    row_handler.create_row(
        user=user,
        table=table,
        values={
            text_field.id: "test",
            date_field.id: "2020-02-01 01:23",
            option_field.id: option_b.id,
        },
    )
    row_handler.create_row(
        user=user,
        table=table,
        values={
            text_field.id: "atest",
            date_field.id: "2020-02-01 01:23",
            option_field.id: option_a.id,
        },
    )
    storage = FileSystemStorage(location=(str(tmpdir)), base_url="http://localhost")

    with patch("baserow.contrib.database.export.handler.default_storage", new=storage):
        run_time = make_aware(parse_datetime("2020-02-01 01:00"), timezone=utc)
        # DRF uses some custom internal date time formatting, use the field itself
        # so the test doesn't break if we set a different default timezone format etc
        expected_expiry_time = DateTimeField().to_representation(
            run_time + timezone.timedelta(minutes=settings.EXPORT_FILE_EXPIRE_MINUTES)
        )
        with freeze_time(run_time):
            with capture_on_commit_callbacks(execute=True):
                response = api_client.post(
                    reverse(
                        "api:database:export:export_view",
                        kwargs={"view_id": grid_view.id},
                    ),
                    data={
                        "exporter_type": "xml",
                        "xml_charset": "utf-8",
                    },
                    format="json",
                    HTTP_AUTHORIZATION=f"JWT {token}",
                )
            response_json = response.json()
            assert "id" in response_json
            job_id = response_json["id"]
            assert response_json == {
                "id": job_id,
                "expires_at": expected_expiry_time,
                "exported_file_name": None,
                "exporter_type": "xml",
                "progress_percentage": 0.0,
                "status": "pending",
                "table": table.id,
                "view": grid_view.id,
                "url": None,
            }
            response = api_client.get(
                reverse("api:database:export:get", kwargs={"job_id": job_id}),
                format="json",
                HTTP_AUTHORIZATION=f"JWT {token}",
            )
            response_json = response.json()
            assert "exported_file_name" in response_json
            filename = response_json["exported_file_name"]
            assert response_json == {
                "id": job_id,
                "expires_at": expected_expiry_time,
                "exported_file_name": filename,
                "exporter_type": "xml",
                "progress_percentage": 1.0,
                "status": "complete",
                "table": table.id,
                "view": grid_view.id,
                "url": f"http://localhost:8000/media/export_files/{filename}",
            }

            file_path = tmpdir.join(settings.EXPORT_FILES_DIRECTORY, filename)
            assert file_path.isfile()
            expected = """<?xml version="1.0" encoding="utf-8" ?><rows>
    <row>
        <id>2</id>
        <text_field>atest</text_field>
        <option_field>A</option_field>
        <date_field>02/01/2020 01:23</date_field>
    </row>
    <row>
        <id>1</id>
        <text_field>test</text_field>
        <option_field>B</option_field>
        <date_field>02/01/2020 01:23</date_field>
    </row>
</rows>
"""
            with open(file_path, "r", encoding="utf-8") as written_file:
                assert written_file.read() == expected
