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
                ('uids', models.CharField(max_length=500)),
                ('new_content', models.CharField(max_length=150)),
                ('pub_date', models.DateTimeField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Sequence',
            fields=[
                ('sid', models.AutoField(serialize=False, primary_key=True)),
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
                ('uid', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=40)),
                ('n_apr', models.PositiveIntegerField(default=0)),
                ('n_cor', models.PositiveIntegerField(default=0)),
                ('password', models.CharField(max_length=40)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('vid', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=40)),
                ('lang', models.CharField(max_length=5)),
                ('sub_langs', models.CharField(max_length=50)),
                ('pub_date', models.DateTimeField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='sequence',
            name='vid',
            field=models.ForeignKey(to='video.Video'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='correction',
            name='sid',
            field=models.ForeignKey(to='video.Sequence'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='correction',
            name='vid',
            field=models.ForeignKey(to='video.Video'),
            preserve_default=True,
        ),
    ]
