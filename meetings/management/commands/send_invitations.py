from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
import requests
import json
from base64 import b64encode
from random import shuffle
from math import ceil

from meetings.models import Donor
from .send_invitation import send_invitation


class Command(BaseCommand):
    help = 'Send invitations'

    def handle(self, *args, **options):
        donors = list(Donor.objects.filter(mail_sent=False).all())

        mails = 0
        for donor in donors:
            usd_amount = float(donor.amount)
            if donor.currency == 'MXN':
                usd_amount /= 24.2
            elif donor.currency == 'GBP':
                usd_amount /= 0.9
            elif donor.currency == 'CAD':
                usd_amount /= 1.5
            elif donor.currency == 'DKK':
                usd_amount /= 6.9
            elif donor.currency == 'EUR':
                usd_amount /= 0.92
            usd_amount = ceil(usd_amount)

            if donor.campaign == 166894 and usd_amount >= 40:
                self.stdout.write('{} {} donated {} USD'.format(donor.first_name, donor.last_name, usd_amount))

                send_invitation(
                    self,
                    '{} {}'.format(donor.first_name, donor.last_name),
                    donor.email,
                    usd_amount,
                )

                donor.mail_sent = True
                donor.save()

        self.stdout.write('{} donors. {} mails sent'.format(len(donors), mails))
