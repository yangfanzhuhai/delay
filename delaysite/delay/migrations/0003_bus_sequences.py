# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('delay', '0002_timetable'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bus_sequences',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('route', models.CharField(max_length=64)),
                ('run', models.IntegerField()),
                ('sequence', models.IntegerField()),
                ('stop_code_lbsl', models.CharField(max_length=64)),
                ('bus_stop_code', models.CharField(max_length=64)),
                ('naptan_atco', models.CharField(max_length=64)),
                ('stop_name', models.CharField(max_length=64)),
                ('location_easting', models.IntegerField()),
                ('location_northing', models.IntegerField()),
                ('heading', models.IntegerField()),
                ('virtual_bus_stop', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
