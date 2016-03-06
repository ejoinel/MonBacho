# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MonBacho', '0022_auto_20160228_1224'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='slug',
            field=models.SlugField(),
        ),
        migrations.AlterField(
            model_name='exam',
            name='year_exam',
            field=models.IntegerField(default=b'2016', choices=[(2016, b'2016'), (2015, b'2015'), (2014, b'2014'), (2013, b'2013'), (2012, b'2012'), (2011, b'2011')]),
        ),
    ]
