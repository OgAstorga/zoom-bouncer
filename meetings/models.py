from django.db import models


class Meeting(models.Model):
    meeting_id = models.BigIntegerField(primary_key=True)
    zoom_id = models.BigIntegerField(null=True)
    password = models.CharField(max_length=20)
    join_url = models.CharField(max_length=256, null=True)
    scheduled_date = models.DateTimeField(null=True)


class Ticket(models.Model):
    token = models.CharField(primary_key=True, max_length=12)
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE)
    usages = models.IntegerField(default=0)
    max_usages = models.IntegerField(default=3)


class Donor(models.Model):
    id = models.IntegerField(primary_key=True)
    campaign = models.IntegerField(null=True)
    first_name = models.CharField(max_length=512)
    last_name = models.CharField(max_length=512)
    email = models.CharField(max_length=512)
    amount = models.CharField(max_length=9)
    currency = models.CharField(max_length=5)
    donation_date = models.CharField(max_length=50, null=True)
    mail_sent = models.BooleanField(default=False, db_index=True)
