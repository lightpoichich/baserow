import os
import tempfile
from pathlib import Path
from unittest.mock import patch, call

import pytest
from django.db import connection
from freezegun import freeze_time

from baserow.contrib.database.table.models import Table
from baserow.core.management.backup.backup_runner import BaserowBackupRunner
from baserow.core.trash.handler import TrashHandler


@pytest.mark.django_db(transaction=True)
def test_can_backup_and_restore_baserow_reverting_changes(data_fixture, environ):
    runner = BaserowBackupRunner(
        host=connection.settings_dict["HOST"],
        database=connection.settings_dict["NAME"],
        username=connection.settings_dict["USER"],
        port=connection.settings_dict["PORT"],
        jobs=1,
    )
    environ["PGPASSWORD"] = connection.settings_dict["PASSWORD"]

    table, fields, rows = data_fixture.build_table(
        columns=[
            ("Name", "text"),
        ],
        rows=[["A"], ["B"], ["C"], ["D"]],
    )
    table_to_delete, _, _ = data_fixture.build_table(
        columns=[
            ("Name", "text"),
        ],
        rows=[["A"], ["B"], ["C"], ["D"]],
    )
    deleted_table_name = table_to_delete.get_database_table_name()

    with tempfile.TemporaryDirectory() as temporary_directory_name:
        backup_loc = temporary_directory_name + "/backup.tar.gz"
        # With a batch size of 1 we expect 3 separate pg_dumps to be run.
        runner.backup_baserow(backup_loc, 1)
        assert Path(backup_loc).is_file()

        model = table.get_model(attribute_names=True)

        # Add a new row after we took the back-up that we want to reset by restoring.
        model.objects.create(**{"name": "E"})
        # Delete a table to check it is recreated.
        TrashHandler.permanently_delete(table_to_delete)

        assert model.objects.count() == 5
        assert Table.objects.count() == 1
        assert deleted_table_name not in connection.introspection.table_names()

        # --clean will make pg_restore overwrite existing db objects, not safe for
        # general usage as it will not delete tables/relations created after the
        # backup.
        runner.restore_baserow(backup_loc, ["--clean", "--if-exists"])

        # The row we made after the backup has gone
        assert model.objects.count() == 4
        # The table we deleted has been restored
        assert Table.objects.count() == 2
        assert deleted_table_name in connection.introspection.table_names()


@patch("tempfile.TemporaryDirectory")
@patch("psycopg2.connect")
@patch("subprocess.check_output")
def test_backup_baserow(
    mock_check_output, mock_connect, mock_tempfile, fs, data_fixture, environ
):

    with mock_connect() as conn:
        with conn.cursor() as cursor:
            cursor.fetchall.return_value = [("public.database_table_2",)]

    fs.create_dir("/fake_tmp_dir")
    mock_tempfile.return_value.__enter__.return_value = "/fake_tmp_dir"
    dbname = connection.settings_dict["NAME"]
    host = connection.settings_dict["HOST"]
    user = connection.settings_dict["USER"]
    port = connection.settings_dict["PORT"]
    runner = BaserowBackupRunner(
        host=host,
        database=dbname,
        username=user,
        port=port,
        jobs=1,
    )
    with freeze_time("2020-01-02 12:00"):
        runner.backup_baserow()
    assert os.path.exists(f"baserow_backup_{dbname}_2020-01-02_12-00-00.tar.gz")
    assert mock_check_output.call_count == 2
    mock_check_output.assert_has_calls(
        [
            call(
                [
                    "pg_dump",
                    f"--host={host}",
                    f"--dbname={dbname}",
                    f"--port={port}",
                    f"--username={user}",
                    "-Fd",
                    "--jobs=1",
                    "-w",
                    "--exclude-table=database_table_*",
                    "--exclude-table=database_relation_*",
                    "--file=/fake_tmp_dir/everything_but_user_tables/",
                ]
            ),
            call(
                [
                    "pg_dump",
                    f"--host={host}",
                    f"--dbname={dbname}",
                    f"--port={port}",
                    f"--username={user}",
                    "-Fd",
                    "--jobs=1",
                    "-w",
                    "--table=public.database_table_2",
                    "--file=/fake_tmp_dir/user_tables_batch_0/",
                ],
            ),
        ]
    )
