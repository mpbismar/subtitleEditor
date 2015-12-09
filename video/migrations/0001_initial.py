# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Correction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('vid', models.PositiveIntegerField(serialize=False)),
                ('sid', models.PositiveIntegerField(serialize=False)),
                ('uids', models.CharField(max_length=500)),
                ('new_content', models.CharField(max_length=150)),
                ('pub_date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Sequence',
            fields=[
                ('sid', models.PositiveIntegerField(unique=True, serialize=False, primary_key=True, db_index=True)),
                ('vid', models.PositiveIntegerField(serialize=False)),
                ('lang', models.CharField(max_length=5)),
                ('content', models.CharField(max_length=150)),
                ('start', models.PositiveIntegerField(serialize=False)),
                ('end', models.PositiveIntegerField(serialize=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('uid', models.PositiveIntegerField(unique=True, serialize=False, primary_key=True, db_index=True)),
                ('name', models.CharField(max_length=40)),
                ('n_votes', models.PositiveIntegerField(default=0)),
                ('n_corr', models.PositiveIntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('vid', models.PositiveIntegerField(unique=True, serialize=False, primary_key=True, db_index=True)),
                ('name', models.CharField(max_length=40)),
                ('lang', models.CharField(max_length=5)),
                ('sub_langs', models.CharField(max_length=50)),
                ('pub_date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
