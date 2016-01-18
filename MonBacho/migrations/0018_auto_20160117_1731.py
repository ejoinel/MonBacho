# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MonBacho', '0017_remove_documentfile_file_path'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documentfile',
            name='file_value',
            field=models.FileField(upload_to=b'photo/'),
        ),
    ]
