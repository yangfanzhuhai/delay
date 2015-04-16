# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import djgeojson.fields


class Migration(migrations.Migration):

    dependencies = [
        ('delay', '0005_auto_20150414_1707'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bus_stop',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('geom', djgeojson.fields.PointField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
