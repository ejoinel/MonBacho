# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MonBacho', '0007_auto_20151222_0023'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='school',
            field=models.ForeignKey(blank=True, to='MonBacho.School', null=True),
        ),
    ]
