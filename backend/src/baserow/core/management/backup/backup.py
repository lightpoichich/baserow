import math
import re
import subprocess
import tarfile
import tempfile
from pathlib import Path
from typing import Optional, List

import psycopg2
from django.utils import timezone

from baserow.contrib.database.fields.models import LinkRowField
from baserow.contrib.database.table.models import Table


def run(command):
    print(" ".join(command))
    subprocess.check_output(command)


class BackupPostgresCommand:
    def __init__(
        self,
        host: str,
        database: str,
        username: str,
        port: str,
        jobs: int,
        additional_args: Optional[List[str]],
    ):
        self.host = host
        self.database = database
        self.username = username
        self.port = port
        self.jobs = jobs
        self.additional_args = additional_args or []

    def get_pg_args(self) -> List[str]:
        params = [
            "--host=" + self.host,
            "--dbname=" + self.database,
            "--port=" + self.port,
            "--username=" + self.username,
            # Run in directory mode so we can do parallel dumps using the jobs flag.
            "-Fd",
            "--jobs=" + str(self.jobs),
            # Force non-interactive password input as we will be running many
            # separate pg_dump commands and entering the password over and over is
            # horrible.
            "-w",
        ]
        return params + self.additional_args

    def as_pg_dump_cmd(self, extra_commands: List[str]) -> List[str]:
        return ["pg_dump"] + self.get_pg_args() + extra_commands

    def as_pg_restore_cmd(self, extra_commands: List[str]) -> List[str]:
        return ["pg_restore"] + self.get_pg_args() + extra_commands


def backup_everything_but_user_tables(
    args: BackupPostgresCommand, temporary_directory_name: str
):
    run(
        args.as_pg_dump_cmd(
            [
                f"--exclude-table={Table.USER_TABLE_DATABASE_NAME_PREFIX}*",
                f"--exclude-table={LinkRowField.THROUGH_DATABASE_TABLE_PREFIX}*",
                f"--file={temporary_directory_name}/everything_but_user_tables/",
            ]
        ),
    )


def get_sorted_user_tables_names(args: BackupPostgresCommand) -> List[str]:
    conn = None
    cur = None
    try:
        conn = psycopg2.connect(
            host=args.host,
            port=args.port,
            database=args.database,
            user=args.username,
        )
        cur = conn.cursor()

        table_prefix_regex_escaped = re.escape(Table.USER_TABLE_DATABASE_NAME_PREFIX)
        through_table_regex_escaped = re.escape(
            LinkRowField.THROUGH_DATABASE_TABLE_PREFIX
        )
        # Ensure we order the tables by their numerical ID for consistent and
        # understandable back-up ordering.
        cur.execute(
            f"""SELECT CONCAT(table_schema, '.', table_name)
    FROM information_schema.tables
    WHERE table_name ~ '^{table_prefix_regex_escaped}.*$' or
          table_name ~ '^{through_table_regex_escaped}.*$'
    ORDER BY table_schema,
             substring(table_name FROM '[a-zA-Z]+'),
             substring(table_name FROM '[0-9]+')::int"""
        )
        return [r[0] for r in cur.fetchall()]
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


def backup_user_tables_in_batches(
    batch_size: int, args: BackupPostgresCommand, temporary_directory_name: str
):
    sorted_user_table_names = get_sorted_user_tables_names(args)
    num_batches = math.ceil(len(sorted_user_table_names) / batch_size)
    for batch_num in range(num_batches):
        tables_to_dump_this_batch = sorted_user_table_names[
            batch_num * batch_size : (batch_num + 1) * batch_size
        ]
        pg_dump_tables_include_arg = [f"--table={t}" for t in tables_to_dump_this_batch]
        run(
            args.as_pg_dump_cmd(
                pg_dump_tables_include_arg
                + [f"--file={temporary_directory_name}/user_tables_batch_{batch_num}/"]
            ),
        )


def restore_everything_but_user_tables(
    args: BackupPostgresCommand, extracted_backup_location: Path
):
    run(
        args.as_pg_restore_cmd(
            [
                f"{str(extracted_backup_location)}/everything_but_user_tables/",
            ]
        ),
    )


def restore_user_tables_from_batch_back_ups(
    args: BackupPostgresCommand, temporary_directory_name: Path
):
    for child in temporary_directory_name.iterdir():
        if child.name != "everything_but_user_tables":
            run(
                args.as_pg_restore_cmd(
                    [
                        str(child),
                    ]
                ),
            )


def calculate_batch_size():
    return 1


def default_backup_location(database):
    now = timezone.now().strftime("%Y-%m-%d_%H-%M-%S")
    return f"baserow_backup_{database}_{now}.tar.gz"


def do_backup(
    args: BackupPostgresCommand,
    backup_file_name: Optional[str],
    batch_size: Optional[int],
):
    backup_file_name = backup_file_name or default_backup_location(args.database)
    batch_size = batch_size or calculate_batch_size()
    try:
        with tarfile.open(backup_file_name, "w:gz") as backup_output_tar:
            with tempfile.TemporaryDirectory() as temporary_directory_name:
                backup_everything_but_user_tables(args, temporary_directory_name)
                backup_user_tables_in_batches(
                    batch_size, args, temporary_directory_name
                )
                backup_internal_folder_name = Path(backup_file_name).name
                backup_output_tar.add(
                    temporary_directory_name, arcname=backup_internal_folder_name
                )
    except Exception as e:
        backup_file_to_cleanup = Path(backup_file_name)
        if backup_file_to_cleanup.is_file():
            backup_file_to_cleanup.unlink()
        raise e


def restore_backup(args: BackupPostgresCommand, backup_file_name: str):
    with tempfile.TemporaryDirectory() as temporary_directory_name:
        with tarfile.open(backup_file_name, "r:gz") as backup_input_tar:
            backup_input_tar.extractall(temporary_directory_name)
        backup_internal_folder_name = Path(backup_file_name).name
        backup_sub_folder = Path(
            temporary_directory_name, backup_internal_folder_name
        ).resolve()
        if not backup_sub_folder.is_dir():
            raise Exception(
                f"Expected to find a folder inside {backup_file_name} called "
                f"{backup_internal_folder_name} but it wasn't there. Is the file you "
                "provided a valid baserow backup file generated by ./baserow "
                "backup_db ?"
            )
        restore_everything_but_user_tables(args, backup_sub_folder)
        restore_user_tables_from_batch_back_ups(args, backup_sub_folder)
