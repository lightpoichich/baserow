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
            "database",
            type=str,
            help="The database connection name to use to connect to the db.",
        )
        parser.add_argument(
            "backup_name",
            type=str,
            help="The name of the folder to store the backup in.",
        )
        parser.add_argument(
            "--actually-run",
            action="store_true",
            help="Provide this flag if you want to actually do the copy. Without this "
            "flag the command will run in a dry run mode and not make any changes.",
        )
        parser.add_argument(
            "--ssl",
            action="store_true",
            help="Provide this flag if psql should be run with sslmode=require",
        )

    def handle(self, *args, **options):
        actually_run = "actually_run" in options and options["actually_run"]
        ssl = "ssl" in options and options["ssl"]

        source = options["database"]
        backup_name = options["backup_name"]
        db_connection = connections[source]
        db_connection_string = connection_string_from_django_connection(db_connection)
        if actually_run:
            print(f"REAL RUN, ABOUT TO BACKUP DATABASE {source} ")
        else:
            print(f"Dry run over db {source} ")

        command = (
            f"pg_basebackup {db_connection_string} -D {backup_name} -F t -z -l "
            f'"baserow backup run at `date`" -X stream -R -P'
        )

        if actually_run:
            env_variables = {"PGPASSWORD": db_connection.settings_dict["PASSWORD"]}
            if ssl:
                env_variables["PGSSLMODE"] = "require"
            run(command, env_variables)
        else:
            print(f"Would have run {command}.")
