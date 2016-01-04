# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MonBacho', '0014_auto_20160103_0644'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documentfile',
            name='description',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
