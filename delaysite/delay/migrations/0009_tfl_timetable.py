# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('delay', '0008_auto_20150416_1718'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tfl_timetable',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('linename', models.CharField(db_index=True, max_length=16)),
                ('day', models.CharField(db_index=True, max_length=32)),
                ('run', models.IntegerField()),
                ('sequence', models.IntegerField()),
                ('stop_name', models.CharField(max_length=64)),
                ('arrival_time', models.CharField(max_length=64)),
                ('cummulative_travel_time', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
