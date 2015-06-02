# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('delay', '0022_auto_20150602_0853'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tfl_timetable',
            old_name='travel_time',
            new_name='average_travel_time',
        ),
        migrations.AddField(
            model_name='tfl_timetable',
            name='cumulative_travel_time',
            field=models.IntegerField(default=None),
            preserve_default=False,
        ),
    ]
