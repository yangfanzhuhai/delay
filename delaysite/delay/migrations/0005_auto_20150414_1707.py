# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('delay', '0004_auto_20150319_1319'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timetable',
            name='day',
            field=models.CharField(db_index=True, max_length=9),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='timetable',
            name='end_stop',
            field=models.CharField(db_index=True, max_length=64),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='timetable',
            name='hour',
            field=models.IntegerField(db_index=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='timetable',
            name='start_stop',
            field=models.CharField(db_index=True, max_length=64),
            preserve_default=True,
        ),
    ]
