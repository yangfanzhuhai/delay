# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('delay', '0010_tfl_timetable_departure_time_from_origin'),
    ]

    operations = [
        migrations.AddField(
            model_name='tfl_timetable',
            name='naptan_atco',
            field=models.CharField(max_length=64, default=''),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='tfl_timetable',
            name='departure_time_from_origin',
            field=models.CharField(max_length=64, default=''),
            preserve_default=True,
        ),
    ]
