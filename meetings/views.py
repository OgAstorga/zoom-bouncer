from django.shortcuts import render
from django.http import HttpResponse
from .models import Ticket, Donor
from datetime import datetime, timezone
from math import ceil
import json


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

        return render(request, 'meetings/ticket-redirect.html', {
            'meeting': meeting
        })
    else:
        return render(request, 'meetings/ticket-limitreached.html')


def summary(request):
    donors = Donor.objects.all()

    campaign = int(request.GET.get('campaign', 166894))

    count = 0
    total = 0
    detail = dict()
    for donor in donors:
        if donor.campaign != campaign:
            continue

        if donor.currency not in detail:
            detail[donor.currency] = 0.0

        detail[donor.currency] += float(donor.amount)

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

        count += 1
        total += usd_amount

    answer = {
        "count": count,
        "total": total,
        'detail': list(detail.items()),
    }

    return HttpResponse(json.dumps(answer), content_type="application/json")
