# Generated by Django 3.0.5 on 2020-05-04 03:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Meeting',
            fields=[
                ('meeting_id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('password', models.CharField(max_length=20)),
                ('scheduled_date', models.DateTimeField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('token', models.CharField(max_length=12, primary_key=True, serialize=False)),
                ('usages', models.IntegerField(default=0)),
                ('max_usages', models.IntegerField(default=3)),
                ('meeting', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='meetings.Meeting')),
            ],
        ),
    ]
