import sys
import json
import argparse

from django.core.management.base import BaseCommand

from baserow.core.models import Group
from baserow.core.handler import CoreHandler


class Command(BaseCommand):
    help = (
        'Imports applications in JSON format and adds them to a group.'
    )

    def add_arguments(self, parser):
        parser.add_argument(
            'group_id',
            type=int,
            help='The id of the group where the newly created applications must be '
                 'added to.'
        )
        parser.add_argument(
            'json',
            nargs='?',
            type=argparse.FileType('r'),
            default=sys.stdin
        )

    def handle(self, *args, **options):
        group_id = options['group_id']
        json_file = options['json']

        try:
            group = Group.objects.get(pk=group_id)
        except Group.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'The group with id {group_id} was not '
                                               f'found.'))
            sys.exit(1)

        content = json.load(json_file)
        handler = CoreHandler()
        application = handler.import_application_to_group(group, content)
        self.stdout.write(f'{len(application)} applications have been imported.')
