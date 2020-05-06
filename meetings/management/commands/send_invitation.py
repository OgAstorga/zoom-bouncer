from django.conf import settings
from django.core import mail
from django.core.management.base import BaseCommand, CommandError
from django.template.loader import render_to_string
from django.template import TemplateDoesNotExist
from yuid import yuid

from meetings.models import Meeting, Ticket

def send_invitation(self, subject_name, subject_email, donation):
    ticket_ammount = min(donation // 40, 5)

    self.stdout.write('Generating {} tickets for {}'.format(ticket_ammount, subject_email))

    meeting = Meeting.objects.all()[0]

    tickets = []
    for i in range(ticket_ammount):
        ticket = Ticket(
            token=yuid(),
            meeting=meeting,
            max_usages=3,
        )
        ticket.save()
        tickets.append(ticket)

    # render mail
    base_url = settings.PUBLIC_BASE_URL
    html_email = None
    html_email = render_to_string('invitation.html', {
        'subject_name': subject_name,
        'tickets': list(map(lambda t: "{}/ticket/{}".format(base_url, t.token), tickets)),
    })

    # send mail
    connection = mail.get_connection()
    connection.open()

    email = mail.EmailMultiAlternatives(
        'Thank you. Here are your tickets',
        'Body goes here',
        settings.EMAIL_ADDRESS,
        [subject_email],
        connection=connection,
    )
    email.attach_alternative(html_email, 'text/html')
    email.send()

    self.stdout.write(self.style.SUCCESS('mail sent'))


class Command(BaseCommand):
    help = 'Sends invitation links to user'

    def add_arguments(self, parser):
        parser.add_argument('name', type=str)
        parser.add_argument('email', type=str)
        parser.add_argument('donation', type=int)

    def handle(self, *args, **options):
        subject_name = options['name']
        subject_email = options['email']
        donation = options['donation']

        send_invitation(self, subject_name, subject_email, donation)
