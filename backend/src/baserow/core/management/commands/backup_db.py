from django.core.management.base import BaseCommand

from baserow.core.management.backup.backup import do_backup, BackupPostgresCommand


class Command(BaseCommand):
    help = """
        Backs up a Baserow database into a single compressed archive which can be
        restored using the restore_db Baserow management command. To provide the
        database password you must either have a valid .pgpass file containing the
        password for the requested connection in the expected postgres location (see
        https://www.postgresql.org/docs/current/libpq-pgpass.html) or set the
        PGPASSFILE environment variable.

        WARNING: This command is only safe to run on a database which is not actively
        being updated and not connected to a running version of Baserow for the
        duration of the back-up.

        This command splits the back-up into multiple `pg_dump` runs to export the
        databases tables in batches and so might generate an inconsistent back-up if
        database changes occur partway through the run. Additionally when tables are
        being backed up this command will hold an ACCESS SHARE lock over them, meaning
        users will see errors if they attempt to delete tables or edit fields.

        The back-up is split into batches as often Baserow database's can end up with
        large numbers of tables and a single run of `pg_dump` over the entire database
        will run out of shared memory and fail.
        """

    def create_parser(self, prog_name, subcommand, **kwargs):
        kwargs["add_help"] = False
        return super().create_parser(prog_name, subcommand, **kwargs)

    def add_arguments(self, parser):
        # Override the help flag so -h can be used for host like pg_dump
        parser.add_argument(
            "--help", action="help", help="Show this help message and exit."
        )
        parser.add_argument(
            "--batch-size",
            type=int,
            default=False,
            dest="batch-size",
            help="The number of tables to back_up per each `pg_dump` command. If you "
            "are encountering out of shared memory errors then you can either "
            "lower this value or increase your databases "
            "`max_locks_per_transaction` setting. Increasing this setting will"
            "increase the speed of the back-up.",
        )
        # The arguments below are meant to match `pg_dump`s arguments in name as this
        # management command is a simple batching/looping wrapper over `pg_dump`.
        parser.add_argument(
            "-j",
            "--jobs",
            type=int,
            default=1,
            dest="jobs",
            help="Run each `pg_dump` command in parallel by dumping this number of "
            "tables simultaneously per batch back-up run. This option reduces "
            "the time of the backup but it also increases the load on the database"
            "server. Please read the `pg_dump` documentation for this argument "
            "for further details.",
        )
        parser.add_argument(
            "-f",
            "--file",
            type=str,
            default=False,
            dest="file",
            help="Send the backup to the specified file. If not given then "
            "backups will be saved to the working directory with a file name of "
            "`baserow_backup_{database}_{time}.tar.gz`",
        )
        parser.add_argument(
            "-h",
            "--host",
            type=str,
            required=True,
            dest="host",
            help="The host name of the machine on which the database is running.",
        )
        parser.add_argument(
            "-d",
            "--database",
            required=True,
            type=str,
            dest="database",
            help="Specifies the name of the database to connect to.",
        )
        parser.add_argument(
            "-U",
            "--username",
            required=True,
            type=str,
            dest="username",
            help="The username to connect to the database as.",
        )
        parser.add_argument(
            "-p",
            "--port",
            type=str,
            default="5432",
            dest="port",
            help="Specifies the TCP port or local Unix domain socket file on which "
            "the server is listening for connections.",
        )
        parser.add_argument(
            "additional_pg_dump_args",
            nargs="*",
            help="Any further args specified here will be directly "
            "passed to each call of `pg_dump` which this back_up tool "
            "runs, please see https://www.postgresql.org/docs/11/app-pgdump.html for "
            "all the available options. Please be careful as arguments provided "
            "here will override arguments passed to `pg_dump` internally by "
            "this tool such as -w, -T and -t causing errors and undefined behavior.",
        )

    def handle(self, *args, **options):
        host = options["host"]
        database = options["database"]
        username = options["username"]
        port = options["port"]
        batch_size = options["batch-size"]
        file = options["file"]
        jobs = options["jobs"]
        additional_args = options["additional_pg_dump_args"]

        dump_args = BackupPostgresCommand(
            host,
            database,
            username,
            port,
            jobs,
            additional_args,
        )
        do_backup(dump_args, file, batch_size)
