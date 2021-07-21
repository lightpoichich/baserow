import math
from subprocess import Popen

from django.core.management.base import BaseCommand
from django.db import connections


def run(command, password, ssl_mode=False):
    env = {"PGPASSWORD": password}
    if ssl_mode:
        env["PGSSLMODE"] = "require"
    proc = Popen(command, shell=True, env=env)
    proc.wait()


def connection_string_from_django_connection(django_connection):
    settings_dict = django_connection.settings_dict
    params = [
        "-h " + settings_dict["HOST"],
        "-d " + settings_dict["NAME"],
        "-p " + settings_dict["PORT"],
        "-U " + settings_dict["USER"],
        "-w",  # Specify the password is not to be provided interactively as we are
        # setting the PGPASSWORD env variable instead.
    ]
    return " ".join(params)


class Command(BaseCommand):
    help = "Copies all the tables from one django database connection to another."

    def add_arguments(self, parser):
        parser.add_argument(
            "--source_connection",
            type=str,
            required=True,
            help="The django database connection name to copy tables from the public "
            "schema.",
        )
        parser.add_argument(
            "--target_connection",
            type=str,
            required=True,
            help="The django database connection name to copy tables to the public "
            "schema.",
        )
        parser.add_argument(
            "--batch_size",
            type=int,
            required=True,
            help="The number of tables to transfer at once in each pg_dump batch.",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Provide this flag to show a dry run report of the tables that would "
            "be copied without this flag.",
        )
        parser.add_argument(
            "--ssl",
            action="store_true",
            help="Provide this flag if ssl should be enabled via sslmode=require",
        )

    def handle(self, *args, **options):
        dry_run = "dry_run" in options and options["dry_run"]
        ssl = "ssl" in options and options["ssl"]
        batch_size = options["batch_size"]

        source = options["source_connection"]
        source_connection = connections[source]
        source_tables = source_connection.introspection.table_names()
        source_connection_params = connection_string_from_django_connection(
            source_connection
        )
        source_db_name = source_connection.settings_dict["NAME"]

        target = options["target_connection"]
        target_connection = connections[target]
        target_connection_params = connection_string_from_django_connection(
            target_connection
        )
        target_tables = set(target_connection.introspection.table_names())
        target_db_name = target_connection.settings_dict["NAME"]

        if dry_run:
            self.stdout.write(
                self.style.WARNING(
                    "Dry run... If --actually-run was provided then would"
                    f" copy {source_db_name} to {target_db_name}"
                )
            )
        else:
            self.stdout.write(
                self.style.NOTICE(
                    f"REAL RUN, ABOUT TO COPY TABLES FROM {source_db_name} to "
                    f"{target_db_name}"
                )
            )

        if ssl:
            self.stdout.write(self.style.SUCCESS("Running with sslmode=require"))

        count = 0
        num_batches = math.ceil(len(source_tables) / batch_size)
        for batch_num in range(num_batches):
            batch = set(
                source_tables[batch_num * batch_size : (batch_num + 1) * batch_size]
            )
            tables_not_in_target_db = batch.difference(target_tables)
            num_to_copy = len(tables_not_in_target_db)
            count += num_to_copy
            self.stdout.write(
                self.style.SUCCESS(f"Importing {num_to_copy} tables in " f"one go")
            )
            if num_to_copy > 0:
                table_str = ""
                for table in tables_not_in_target_db:
                    table_str += f" -t public.{table}"

                command = (
                    f"pg_dump {source_connection_params} {table_str} | "
                    f"psql {target_connection_params}"
                )
                if dry_run:
                    self.stdout.write(f"Would have run {command}")
                else:
                    self.stdout.write(f"Running command: {command}")
                    run(
                        command,
                        source_connection.settings_dict["PASSWORD"],
                        ssl_mode=ssl,
                    )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f"Skipping import of batch {batch_num} as all tables were "
                        "already in the target database."
                    )
                )
        self.stdout.write(self.style.SUCCESS(f"Successfully copied {count} tables."))
