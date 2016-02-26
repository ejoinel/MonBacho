# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MonBacho', '0020_auto_20160226_0003'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documentfile',
            name='image',
            field=models.ImageField(upload_to=b'photo/', verbose_name=b'image'),
        ),
    ]
