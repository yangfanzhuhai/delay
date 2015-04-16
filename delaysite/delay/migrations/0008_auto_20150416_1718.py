# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('delay', '0007_auto_20150416_1447'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Predictions',
        ),
        migrations.AddField(
            model_name='bus_sequences',
            name='average_travel_time',
            field=models.DecimalField(max_digits=11, default=0.0, decimal_places=1),
            preserve_default=True,
        ),
    ]
