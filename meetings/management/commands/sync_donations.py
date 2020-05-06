from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
import requests
import json
from base64 import b64encode

from meetings.models import Donor


class Command(BaseCommand):
    help = 'Sync donors'

    def handle(self, *args, **options):
        AuthorizationHeader = '{}:{}'.format(settings.DONOR_USER, settings.DONOR_PASSWORD)
        response = requests.get('https://donorbox.org/api/v1/donations?per_page=100', headers={
            'Authorization': 'Basic {}'.format(b64encode(AuthorizationHeader.encode()).decode('ascii'))
        })

        donations = response.json()

        self.stdout.write("Fetch donors: {} donors".format(len(donations)))

        synced_donors = 0
        for donation in donations:
            donor = None
            try:
                donor = Donor.objects.get(id=donation['id'])
            except Donor.DoesNotExist:
                pass

            if not donor:
                donor = Donor(
                    id=donation['id'],
                    first_name=donation['donor']['first_name'],
                    last_name=donation['donor']['last_name'],
                    email=donation['donor']['email'],
                    amount=donation['amount'],
                    currency=donation['currency'],
                )

                donor.save()

                synced_donors += 1

        self.stdout.write("New donors: {} donors".format(synced_donors))
