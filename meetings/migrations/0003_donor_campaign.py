# Generated by Django 3.0.6 on 2020-05-06 04:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meetings', '0002_donor'),
    ]

    operations = [
        migrations.AddField(
            model_name='donor',
            name='campaign',
            field=models.IntegerField(null=True),
        ),
    ]