# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MonBacho', '0018_auto_20160117_1731'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='deletion_date',
            field=models.DateTimeField(default=None, null=True),
        ),
    ]
