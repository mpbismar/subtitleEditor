# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-01 17:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Correction',
            fields=[
                ('cid', models.AutoField(primary_key=True, serialize=False)),
                ('uids', models.CharField(max_length=500)),
                ('new_content', models.CharField(max_length=150)),
                ('pub_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Sequence',
            fields=[
                ('sid', models.AutoField(primary_key=True, serialize=False)),
                ('lang', models.CharField(max_length=5)),
                ('content', models.CharField(max_length=150)),
                ('start', models.PositiveIntegerField(serialize=False)),
                ('end', models.PositiveIntegerField(serialize=False)),
                ('rating', models.PositiveIntegerField(default=0)),
                ('pub_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('uid', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=40)),
                ('n_apr', models.PositiveIntegerField(default=0)),
                ('n_cor', models.PositiveIntegerField(default=0)),
                ('password', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('vid', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=40)),
                ('lang', models.CharField(max_length=5)),
                ('sub_langs', models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='sequence',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='video.User'),
        ),
        migrations.AddField(
            model_name='sequence',
            name='vid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='video.Video'),
        ),
        migrations.AddField(
            model_name='correction',
            name='sid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='video.Sequence'),
        ),
        migrations.AddField(
            model_name='correction',
            name='vid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='video.Video'),
        ),
    ]
