# Generated by Django 3.2.16 on 2023-01-26 16:05

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('web_admin', '0002_auto_20230126_1551'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sessions',
            name='date_time',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 1, 26, 16, 5, 21, 421380, tzinfo=utc), null=True),
        ),
    ]