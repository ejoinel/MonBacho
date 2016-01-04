# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MonBacho', '0012_auto_20160103_0523'),
    ]

    operations = [
        migrations.AddField(
            model_name='documentfile',
            name='file_value',
            field=models.FileField(null=True, upload_to=b'photo/'),
        ),
    ]
