# Generated by Django 3.0.6 on 2020-05-08 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meetings', '0004_meeting_join_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='meeting',
            name='zoom_id',
            field=models.BigIntegerField(null=True),
        ),
    ]