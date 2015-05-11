# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('delay', '0016_tfl_timetable_travel_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bus_sequences',
            name='route',
            field=models.CharField(max_length=64, db_index=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='bus_sequences',
            name='run',
            field=models.IntegerField(db_index=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='bus_sequences',
            name='sequence',
            field=models.IntegerField(db_index=True),
            preserve_default=True,
        ),
    ]
