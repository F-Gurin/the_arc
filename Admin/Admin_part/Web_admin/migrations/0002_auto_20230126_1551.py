# Generated by Django 3.2.16 on 2023-01-26 15:51

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_admin', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sessions',
            name='date_time',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 1, 26, 15, 51, 55, 511750), null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='date_of_birth',
            field=models.DateField(default='2023-01-26'),
        ),
    ]
