# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('delay', '0017_auto_20150511_1528'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tfl_timetable',
            old_name='cummulative_travel_time',
            new_name='cumulative_travel_time',
        ),
        migrations.AlterField(
            model_name='bus_sequences',
            name='naptan_atco',
            field=models.CharField(db_index=True, max_length=64),
            preserve_default=True,
        ),
    ]
