import uuid

from django.core.management.base import BaseCommand
from faker import Faker

from baserow.core.user.handler import UserHandler


class Command(BaseCommand):
    help = "Fills baserow with random users."

    def add_arguments(self, parser):
        parser.add_argument(
            "limit", type=int, help="Amount of users that need to be inserted."
        )

    def handle(self, *args, **options):
        limit = options["limit"]
        fake = Faker()
        user_handler = UserHandler()

        email_prefix = (
            "baserow_prefix_to_ensure_we_never_accidentally_email_a_real_person_"
        )
        for i in range(limit):
            user_handler.create_user(
                fake.name(), email_prefix + fake.email(), str(uuid.uuid4())
            )

        self.stdout.write(self.style.SUCCESS(f"{limit} rows have been inserted."))
