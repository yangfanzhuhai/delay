# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('delay', '0014_auto_20150511_1131'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tfl_timetable',
            old_name='linename',
            new_name='route',
        ),
    ]
