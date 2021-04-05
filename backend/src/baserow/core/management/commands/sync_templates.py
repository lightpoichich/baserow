from django.core.management.base import BaseCommand

from baserow.core.handler import CoreHandler


class Command(BaseCommand):
    help = (
        'Synchronizes all JSON file templates in the templates directory with '
        'templates stored in the database.'
    )

    def handle(self, *args, **options):
        CoreHandler().sync_templates()
