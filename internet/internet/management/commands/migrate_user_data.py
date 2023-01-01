from tendo import singleton
from django.core.management.base import BaseCommand
from internet.scripts.upload_user_usage_data import run

SERVICE_NAME = 'migrate_user_data'
mes = singleton.SingleInstance(SERVICE_NAME)


class Command(BaseCommand):
    help = "User Data"

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        run()
