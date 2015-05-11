# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('delay', '0018_auto_20150511_2154'),
    ]

    operations = [
        migrations.AddField(
            model_name='bus_sequences',
            name='cumulative_travel_time',
            field=models.DecimalField(decimal_places=1, max_digits=11, default=0.0),
            preserve_default=True,
        ),
    ]
