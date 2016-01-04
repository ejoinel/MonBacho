# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MonBacho', '0011_auto_20151230_1147'),
    ]

    operations = [
        migrations.CreateModel(
            name='DocumentFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(max_length=100, null=True)),
                ('file_path', models.CharField(max_length=100)),
                ('file_type', models.IntegerField(default=1, choices=[(1, b'image'), (2, b'pdf'), (3, b'video')])),
            ],
            options={
                'db_table': 'DocumentFile',
            },
        ),
        migrations.RemoveField(
            model_name='image',
            name='document',
        ),
        migrations.AddField(
            model_name='exam',
            name='mock_exam',
            field=models.IntegerField(default=1, choices=[(1, b'real'), (2, b'mock')]),
        ),
        migrations.AddField(
            model_name='exam',
            name='year_exam',
            field=models.IntegerField(default=1, choices=[(1, b'2016'), (2, b'2015'), (3, b'2014'), (4, b'2013'), (5, b'2013'), (6, b'2012')]),
        ),
        migrations.AlterField(
            model_name='document',
            name='status',
            field=models.IntegerField(default=1, choices=[(1, b'new'), (2, b'cleared'), (3, b'deleted')]),
        ),
        migrations.DeleteModel(
            name='Image',
        ),
        migrations.AddField(
            model_name='documentfile',
            name='document',
            field=models.ForeignKey(to='MonBacho.Document'),
        ),
    ]
