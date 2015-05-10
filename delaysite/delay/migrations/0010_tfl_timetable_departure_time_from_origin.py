# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('delay', '0009_tfl_timetable'),
    ]

    operations = [
        migrations.AddField(
            model_name='tfl_timetable',
            name='departure_time_from_origin',
            field=models.CharField(max_length=64, default=None),
            preserve_default=False,
        ),
    ]
