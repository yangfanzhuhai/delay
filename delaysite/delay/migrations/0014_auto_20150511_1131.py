# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('delay', '0013_auto_20150510_2248'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tfl_timetable',
            name='arrival_time',
            field=models.DateTimeField(db_index=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='tfl_timetable',
            name='departure_time_from_origin',
            field=models.DateTimeField(db_index=True),
            preserve_default=True,
        ),
    ]
