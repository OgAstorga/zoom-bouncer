import json
import requests

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from meetings.models import Meeting


class Command(BaseCommand):
    help = "Change meeting passwords & update data"


    def handle(self, *args, **options):
        meetings = Meeting.objects.all()
        for meeting in meetings:
            self.handle_meeting(meeting)


    def handle_meeting(self, meeting):
        meeting_id = meeting.zoom_id

        if not meeting_id:
            return

        response = requests.patch(
            "https://api.zoom.us/v2/meetings/{}/".format(meeting_id),
            data=json.dumps({ "password": 123123 }),
            headers={
                "Authorization": "Bearer {}".format(settings.ZOOM_JWT),
                "Content-Type": "application/json",
            }
        )

        if response.status_code != 204:
            self.stdout.write(self.style.ERROR("Unexpected response when updating"))
            self.stdout.write(response.text)

        response = requests.get(
            "https://api.zoom.us/v2/meetings/{}/".format(meeting_id),
            headers={
                "Authorization": "Bearer {}".format(settings.ZOOM_JWT)
            }
        )

        if response.status_code != 200:
            self.stdout.write(self.style.ERROR("Unexpected response when fetching"))
            self.stdout.write(response.text)

        fetched = response.json()

        # update meeting model
        meeting.password = fetched["password"]
        meeting.join_url = fetched["join_url"]
        meeting.save()

        self.stdout.write("{} new password ({}) for meeting {}".format(
            self.style.SUCCESS("SUCCESS"),
            fetched['password'],
            str(fetched['id']),
        ))

