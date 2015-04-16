# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('delay', '0006_bus_stop'),
    ]

    operations = [
        migrations.CreateModel(
            name='Predictions',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
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
                ('day', models.CharField(db_index=True, max_length=9)),
                ('hour', models.IntegerField(db_index=True)),
                ('average_travel_time', models.DecimalField(decimal_places=1, max_digits=11)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.DeleteModel(
            name='Bus_stop',
        ),
    ]
