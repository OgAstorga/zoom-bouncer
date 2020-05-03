from django.db import models


class Meeting(models.Model):
    meeting_id = models.BigIntegerField(primary_key=True)
    password = models.CharField(max_length=20)
    scheduled_date = models.DateTimeField(null=True)


class Ticket(models.Model):
    token = models.CharField(primary_key=True, max_length=12)
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE)
    usages = models.IntegerField(default=0)
    max_usages = models.IntegerField(default=3)
