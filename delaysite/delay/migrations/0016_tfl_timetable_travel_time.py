# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('delay', '0015_auto_20150511_1305'),
    ]

    operations = [
        migrations.AddField(
            model_name='tfl_timetable',
            name='travel_time',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
