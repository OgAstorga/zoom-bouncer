from django.shortcuts import render
from .models import Ticket
from datetime import datetime, timezone


def ticket_detail(request, token):
    ticket = None
    try:
        ticket = Ticket.objects.get(token=token)
    except Ticket.DoesNotExist:
        pass

    if not ticket:
        return render(request, 'meetings/ticket-404.html');

    meeting = ticket.meeting

    now = datetime.now(timezone.utc)

    if now < meeting.scheduled_date:
        total_seconds = (meeting.scheduled_date - now).total_seconds()
        total_seconds = int(total_seconds)

        days = total_seconds // (3600 * 24)
        hours = (total_seconds % (3600 * 24)) // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60

        return render(request, 'meetings/ticket-countdown.html', {
            'days': days,
            'hours': hours,
            'minutes': minutes,
            'seconds': seconds
        });

    if ticket.usages < ticket.max_usages:
        ticket.usages += 1
        # ticket.save()

        return render(request, 'meetings/ticket-redirect.html')
    else:
        return render(request, 'meetings/ticket-limitreached.html')

