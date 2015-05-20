# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('delay', '0019_bus_sequences_cumulative_travel_time'),
    ]

    operations = [
        migrations.CreateModel(
            name='Current_timetable',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('start_stop', models.CharField(db_index=True, max_length=64)),
                ('end_stop', models.CharField(db_index=True, max_length=64)),
                ('average_travel_time', models.DecimalField(decimal_places=1, max_digits=11, default=0.0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='bus_sequences',
            name='curr_average_travel_time',
            field=models.DecimalField(decimal_places=1, max_digits=11, default=0.0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='bus_sequences',
            name='curr_cumulative_travel_time',
            field=models.DecimalField(decimal_places=1, max_digits=11, default=0.0),
            preserve_default=True,
        ),
    ]
