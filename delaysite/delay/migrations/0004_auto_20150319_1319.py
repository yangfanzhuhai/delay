# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('delay', '0003_bus_sequences'),
    ]

    operations = [
        migrations.RenameField(
            model_name='timetable',
            old_name='travel_time',
            new_name='average_travel_time',
        ),
    ]
