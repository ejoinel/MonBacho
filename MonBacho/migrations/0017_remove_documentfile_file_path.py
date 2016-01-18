# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MonBacho', '0016_auto_20160106_0246'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='documentfile',
            name='file_path',
        ),
    ]
