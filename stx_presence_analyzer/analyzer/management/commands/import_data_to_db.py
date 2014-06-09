from django.core.management.base import BaseCommand
from optparse import make_option

from stx_presence_analyzer.analyzer import models, utils


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--users',
            action='store_true',
            dest='users',
            default=False,
            help='Imports users'),
        make_option('--presences',
            action='store_true',
            dest='presences',
            default=False,
            help='Imports presences'),
    )

    def handle(self, *args, **options):
        users = utils.parse_users_xml('runtime/data/users.xml')
        presences = utils.get_data('runtime/data/sample_data.csv')

        if options['users']:
            for user in users:
                models.User.objects.get_or_create(
                    user_id=user['user_id'],
                    name=user['name']
                )

        if options['presences']:
            for user in presences:
                for date in presences[user]:
                    models.Presence.objects.get_or_create(
                        user_id=user,
                        day=date,
                        start=presences[user][date]['start'],
                        end=presences[user][date]['end']
                    )
                    print "%s" % (user)