# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MonBacho', '0013_documentfile_file_value'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='exam',
            name='matter',
        ),
        migrations.AddField(
            model_name='document',
            name='matter',
            field=models.ForeignKey(to='MonBacho.ClassTopic', null=True),
        ),
    ]
