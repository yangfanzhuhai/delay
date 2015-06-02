# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('delay', '0021_auto_20150521_2221'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tfl_timetable',
            name='arrival_time',
        ),
        migrations.RemoveField(
            model_name='tfl_timetable',
            name='cumulative_travel_time',
        ),
        migrations.RemoveField(
            model_name='tfl_timetable',
            name='departure_time_from_origin',
        ),
        migrations.AddField(
            model_name='tfl_timetable',
            name='arrival_hour',
            field=models.IntegerField(db_index=True, default=0),
            preserve_default=False,
        ),
    ]
