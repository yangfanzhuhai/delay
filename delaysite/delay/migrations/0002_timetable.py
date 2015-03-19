# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('delay', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Timetable',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_stop', models.CharField(max_length=64)),
                ('end_stop', models.CharField(max_length=64)),
                ('day', models.CharField(max_length=9)),
                ('hour', models.IntegerField()),
                ('travel_time', models.DecimalField(max_digits=11, decimal_places=1)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
