import tempfile
from pathlib import Path

import pytest
from django.db import connection

from baserow.core.management.backup.backup_runner import BaserowBackupRunner


@pytest.mark.django_db(transaction=True)
def test_can_backup_and_restore_baserow_reverting_changes(data_fixture, environ):
    runner = BaserowBackupRunner(
        host=connection.settings_dict["HOST"],
        database=connection.settings_dict["NAME"],
        username=connection.settings_dict["USER"],
        port=connection.settings_dict["PORT"],
        jobs=1,
        # Using the clean flag will make pg_restore reset tables back to the old data.
        additional_pg_tool_args=["--clean"],
    )
    environ["PGPASSWORD"] = connection.settings_dict["PASSWORD"]

    table, fields, rows = data_fixture.build_table(
        columns=[
            ("Name", "text"),
        ],
        rows=[["A"], ["B"], ["C"], ["D"]],
    )

    with tempfile.TemporaryDirectory() as temporary_directory_name:
        backup_loc = temporary_directory_name + "/backup.tar.gz"
        runner.backup_baserow(backup_loc)
        assert Path(backup_loc).is_file()

        model = table.get_model(attribute_names=True)

        # Add a new row after we took the back-up that we want to reset by restoring.
        model.objects.create(**{"name": "E"})

        assert model.objects.count() == 5

        runner.restore_baserow(backup_loc)

        # The row we made after the backup has gone!
        assert model.objects.count() == 4
