# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import MonBacho.models


class Migration(migrations.Migration):

    dependencies = [
        ('MonBacho', '0021_auto_20160226_0024'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documentfile',
            name='image',
            field=models.ImageField(upload_to=MonBacho.models.upload_function, verbose_name=b'image'),
        ),
        migrations.AlterField(
            model_name='exam',
            name='year_exam',
            field=models.TextField(default=b'2016', choices=[(b'2016', b'2016'), (b'2015', b'2015'), (b'2014', b'2014'), (b'2013', b'2013'), (b'2012', b'2012'), (b'2011', b'2011')]),
        ),
    ]
