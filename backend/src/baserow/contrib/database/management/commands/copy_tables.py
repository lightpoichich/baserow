from subprocess import Popen

from django.core.management.base import BaseCommand
from django.db import connections


def run(command, password):
    print(f"Running {command}")
    proc = Popen(command, shell=True, env={"PGPASSWORD": password})
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
            "source_database",
            type=str,
            help="The database connection name to copy tables from the public schema.",
        )
        parser.add_argument(
            "target_database",
            type=str,
            help="The database connection name to copy tables to the public schema.",
        )
        parser.add_argument(
            "--actually-run",
            action="store_true",
            help="Provide this flag if you want to actually do the copy. Without this "
            "flag the command will run in a dry run mode and not make any changes.",
        )

    def handle(self, *args, **options):
        actually_run = "actually_run" in options and options["actually_run"]

        source = options["source_database"]
        source_connection = connections[source]
        source_tables = source_connection.introspection.table_names()
        source_connection_params = connection_string_from_django_connection(
            source_connection
        )
        source_db_name = source_connection.settings_dict["NAME"]

        target = options["target_database"]
        target_connection = connections[target]
        target_connection_params = connection_string_from_django_connection(
            target_connection
        )
        target_tables = set(target_connection.introspection.table_names())
        target_db_name = target_connection.settings_dict["NAME"]

        if actually_run:
            self.stdout.write(
                self.style.NOTICE(
                    f"REAL RUN, ABOUT TO COPY TABLES FROM {source_db_name} to "
                    f"{target_db_name}"
                )
            )
        else:
            self.stdout.write(
                self.style.WARNING(
                    "Dry run... If --actually-run was provided then would"
                    f" copy {source_db_name} to {target_db_name}"
                )
            )

        count = 0
        for table in source_tables:
            if table not in target_tables:
                count += 1
                self.stdout.write(self.style.SUCCESS(f"Importing {table}"))
                command = (
                    f"pg_dump {source_connection_params} -t public.{table} | "
                    f"psql {target_connection_params}"
                )
                if actually_run:
                    run(
                        command,
                        source_connection.settings_dict["PASSWORD"],
                    )
                else:
                    self.stdout.write(f"Would have run {command}")
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f"Skipping import of {table} as it is already in the target "
                        "database."
                    )
                )
        self.stdout.write(self.style.SUCCESS(f"Successfully copied {count} tables."))
