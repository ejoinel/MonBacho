# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MonBacho', '0006_auto_20151213_2044'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='sex',
            field=models.IntegerField(default=0, choices=[(0, b'Mr'), (1, b'Mme'), (2, b'Mlle')]),
        ),
    ]
