from subprocess import Popen

from django.core.management.base import BaseCommand
from django.db import connections


def run(command, env):
    print(f"Running {command}")
    proc = Popen(command, shell=True, env=env)
    proc.wait()


def connection_string_from_django_connection(django_connection, host_name, port):
    settings_dict = django_connection.settings_dict
    params = [
        "-h " + settings_dict["HOST"] if host_name == "django" else host_name,
        "-p " + settings_dict["PORT"] if port == "django" else port,
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
            "backup_file_name",
            type=str,
            help="The name of the folder to store the backup in.",
        )
        parser.add_argument(
            "host_name",
            type=str,
            help="To use the django connection setting enter django, otherwise the "
            "host name you want to use.",
        )
        parser.add_argument(
            "port",
            type=str,
            help="To use the django connection setting enter django, otherwise the "
            "port you want to use.",
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
        backup_name = options["backup_file_name"]
        host_name = options["host_name"]
        port = options["port"]
        db_connection = connections[source]
        db_connection_string = connection_string_from_django_connection(
            db_connection, host_name, port
        )
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
