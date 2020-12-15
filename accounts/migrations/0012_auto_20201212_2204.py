# Generated by Django 3.1.3 on 2020-12-12 22:04

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_auto_20201212_2203'),
    ]

    operations = [
        migrations.AddField(
            model_name='agentsearch',
            name='call_lower_limit',
            field=models.TimeField(default=datetime.time(0, 0), null=True),
        ),
        migrations.AddField(
            model_name='agentsearch',
            name='call_upper_limit',
            field=models.TimeField(default=datetime.time(0, 5), null=True),
        ),
    ]
