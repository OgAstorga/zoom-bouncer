# Generated by Django 3.0.6 on 2020-05-08 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meetings', '0003_donor_campaign'),
    ]

    operations = [
        migrations.AddField(
            model_name='meeting',
            name='join_url',
            field=models.CharField(max_length=256, null=True),
        ),
    ]
