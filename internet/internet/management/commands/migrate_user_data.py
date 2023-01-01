from tendo import singleton
from django.core.management.base import BaseCommand
from internet.scripts.upload_user_usage_data import run

# will sys.exit(-1) if other instance is running
SERVICE_NAME = 'migrate_user_data'
mes = singleton.SingleInstance(SERVICE_NAME)


class Command(BaseCommand):
    help = "User Data"

    def add_arguments(self, parser):
        pass
        # parser.add_argument('-t', '--type', type=str,
        #                     help='Type of scrapping sync or async')

    def handle(self, *args, **options):
        run()
