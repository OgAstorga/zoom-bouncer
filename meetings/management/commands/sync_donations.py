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
                    campaign=donation['campaign']['id'],
                    first_name=donation['donor']['first_name'],
                    last_name=donation['donor']['last_name'],
                    email=donation['donor']['email'],
                    amount=donation['amount'],
                    currency=donation['currency'],
                    donation_date=donation['donation_date'],
                )

                donor.save()

                synced_donors += 1
            else:
                donor.campaign=donation['campaign']['id']
                donor.first_name=donation['donor']['first_name']
                donor.last_name=donation['donor']['last_name']
                donor.email=donation['donor']['email']
                donor.amount=donation['amount']
                donor.currency=donation['currency']
                donor.donation_date=donation['donation_date']
                donor.save()

        self.stdout.write("New donors: {} donors".format(synced_donors))
