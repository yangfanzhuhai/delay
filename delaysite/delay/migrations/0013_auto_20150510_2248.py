# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('delay', '0012_auto_20150510_2238'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tfl_timetable',
            name='arrival_time',
            field=models.TimeField(db_index=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='tfl_timetable',
            name='departure_time_from_origin',
            field=models.TimeField(db_index=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='tfl_timetable',
            name='naptan_atco',
            field=models.CharField(db_index=True, max_length=64, default=''),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='tfl_timetable',
            name='run',
            field=models.IntegerField(db_index=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='tfl_timetable',
            name='sequence',
            field=models.IntegerField(db_index=True),
            preserve_default=True,
        ),
    ]
