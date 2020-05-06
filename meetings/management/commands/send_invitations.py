from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
import requests
import json
from base64 import b64encode
from random import shuffle
from math import ceil

from meetings.models import Donor


class Command(BaseCommand):
    help = 'Send invitations'

    def add_arguments(self, parser):
        parser.add_argument('job_size', type=int)

    def handle(self, *args, **options):
        donors = list(Donor.objects.filter(mail_sent=False).all())
        shuffle(donors)
        job_size = options['job_size']

        mails = 0
        for i in range(job_size):
            if i >= len(donors):
                break

            donor = donors[i]

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

            self.stdout.write('{} {} donated {} USD'.format(donor.first_name, donor.last_name, usd_amount))

            if usd_amount < 40:
                # Don't send mail
                donor.mail_sent = True
                donor.save()
            else:
                mails += 1
                pass
                # send mail

        self.stdout.write('{} donors. {} mails sent'.format(min(len(donors), job_size), mails))
