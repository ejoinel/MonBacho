# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClassLevel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
                ('sub_category', models.CharField(max_length=30)),
            ],
            options={
                'db_table': 'ClassLevel',
            },
        ),
        migrations.CreateModel(
            name='ClassTopic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
            ],
            options={
                'db_table': 'ClassTopic',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('comment_date', models.DateTimeField(auto_now_add=True)),
                ('comment', models.TextField(max_length=512)),
            ],
            options={
                'db_table': 'Comment',
            },
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.SlugField(max_length=100)),
                ('nb_views', models.IntegerField(default=0)),
                ('name', models.CharField(max_length=100)),
                ('status', models.IntegerField(default=-1)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('deletion_date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'Document',
            },
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('file_path', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'Image',
            },
        ),
        migrations.CreateModel(
            name='Read',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('read_date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'Read',
            },
        ),
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'School',
            },
        ),
        migrations.CreateModel(
            name='Submit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('submit_date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'Submit',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('is_superuser', models.BooleanField(default=False,
                                                     help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('slug', models.SlugField(max_length=100)),
                ('sex', models.IntegerField(default=0, choices=[(b'0', b'Mr'), (b'1', b'Mme'), (b'2', b'Mlle')])),
                ('nb_points', models.IntegerField(default=0)),
                ('birth_date', models.DateField(default=None, null=True, blank=True)),
                ('email', models.EmailField(unique=True, max_length=254, verbose_name=b'email address', db_index=True)),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name=b'date joined')),
                ('is_active', models.BooleanField(default=True, verbose_name=b'active')),
                ('is_admin', models.BooleanField(default=False)),
                ('receive_newsletter', models.BooleanField(default=False, verbose_name=b'receive newsletter')),
                ('groups', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True,
                                                  help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', verbose_name='groups')),
                ('school', models.OneToOneField(null=True, blank=True, to='MonBacho.School')),
                ('user_permissions', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission',
                                                            blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions')),
            ],
            options={
                'db_table': 'User',
            },
        ),
        migrations.CreateModel(
            name='Correction',
            fields=[
                ('document_ptr', models.OneToOneField(parent_link=True, auto_created=True,
                                                      primary_key=True, serialize=False, to='MonBacho.Document')),
                ('text', models.TextField(max_length=1024)),
            ],
            options={
                'db_table': 'Correction',
            },
            bases=('MonBacho.document',),
        ),
        migrations.CreateModel(
            name='Exam',
            fields=[
                ('document_ptr', models.OneToOneField(parent_link=True, auto_created=True,
                                                      primary_key=True, serialize=False, to='MonBacho.Document')),
                ('matter', models.ForeignKey(to='MonBacho.ClassTopic')),
            ],
            options={
                'db_table': 'Exam',
            },
            bases=('MonBacho.document',),
        ),
        migrations.AddField(
            model_name='submit',
            name='document',
            field=models.ForeignKey(related_name='submit_document', to='MonBacho.Document'),
        ),
        migrations.AddField(
            model_name='submit',
            name='user',
            field=models.ForeignKey(related_name='submit_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='read',
            name='document',
            field=models.ForeignKey(related_name='read_document', to='MonBacho.Document'),
        ),
        migrations.AddField(
            model_name='read',
            name='user',
            field=models.ForeignKey(related_name='read_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='image',
            name='document',
            field=models.ForeignKey(default=None, blank=True, to='MonBacho.Document', null=True),
        ),
        migrations.AddField(
            model_name='document',
            name='level',
            field=models.ForeignKey(to='MonBacho.ClassLevel'),
        ),
        migrations.AddField(
            model_name='document',
            name='school',
            field=models.ForeignKey(to='MonBacho.School'),
        ),
        migrations.AddField(
            model_name='document',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='comment',
            name='document',
            field=models.ForeignKey(related_name='comment_document', to='MonBacho.Document'),
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(related_name='comment_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='correction',
            name='exam',
            field=models.ForeignKey(to='MonBacho.Exam'),
        ),
    ]
