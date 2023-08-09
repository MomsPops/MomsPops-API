from django.core.management.base import BaseCommand
from django.db import IntegrityError
import json

from users.models import Account


class Command(BaseCommand):
    help = "Creates account with users and profiles from test data."

    def handle(self, *args, **options):
        with open("users/data/accounts.json") as file:
            for account_data in json.load(file):
                try:
                    account = Account.objects.create_account(**account_data)
                    Account.objects.activate(account)
                except IntegrityError:
                    print(f"Account {account_data['user']['username']} already exists.")
