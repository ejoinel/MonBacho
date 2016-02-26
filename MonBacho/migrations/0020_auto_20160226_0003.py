# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('MonBacho', '0019_auto_20160117_2256'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='documentfile',
            name='file_type',
        ),
        migrations.RemoveField(
            model_name='documentfile',
            name='file_value',
        ),
        migrations.AddField(
            model_name='documentfile',
            name='image',
            field=models.ImageField(default=datetime.datetime(2016, 2, 25, 23, 3, 55, 819594, tzinfo=utc), upload_to=b'photo/', verbose_name=b'Image'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='documentfile',
            name='document',
            field=models.ForeignKey(default=None, to='MonBacho.Document'),
        ),
    ]
