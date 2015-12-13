# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MonBacho', '0005_auto_20151213_1722'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='firstname',
            field=models.SlugField(default=None, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='lastname',
            field=models.SlugField(default=None, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='receive_newsletter',
            field=models.BooleanField(default=True, verbose_name=b'receive newsletter'),
        ),
    ]
