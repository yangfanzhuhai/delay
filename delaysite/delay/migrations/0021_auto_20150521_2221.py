# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('delay', '0020_auto_20150520_1406'),
    ]

    operations = [
        migrations.AddField(
            model_name='current_timetable',
            name='date',
            field=models.DateField(default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='current_timetable',
            name='day',
            field=models.CharField(db_index=True, max_length=9, default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='current_timetable',
            name='hour',
            field=models.IntegerField(db_index=True, default=None),
            preserve_default=False,
        ),
    ]
