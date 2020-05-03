from django.conf import settings
from django.core import mail
from django.core.management.base import BaseCommand, CommandError
from django.template.loader import render_to_string
from django.template import TemplateDoesNotExist


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

        ticket_ammount = donation // 40

        self.stdout.write('Generating {} tickets for {}'.format(ticket_ammount, subject_email))

        '''
        tickets = []
        for i in range(ticket_ammount):
            ticket = Ticket(max_usages=1)
            ticket.save()
            tickets.append(ticket)
        '''

        # render mail
        html_email = None
        html_email = render_to_string('invitation.html', {
            'subject_name': subject_name
        })


        # send mail
        connection = mail.get_connection()
        connection.open()

        email = mail.EmailMultiAlternatives(
            'Hello',
            'Body goes here',
            settings.EMAIL_ADDRESS,
            [subject_email],
            connection=connection,
        )
        email.attach_alternative(html_email, 'text/html')
        email.send()

        self.stdout.write(self.style.SUCCESS('mail sent'))
