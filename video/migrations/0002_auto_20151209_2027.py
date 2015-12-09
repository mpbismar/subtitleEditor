# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='n_corr',
            new_name='n_apr',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='n_votes',
            new_name='n_cor',
        ),
        migrations.AlterField(
            model_name='correction',
            name='pub_date',
            field=models.DateTimeField(auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='correction',
            name='sid',
            field=models.ForeignKey(to='video.Sequence'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='correction',
            name='vid',
            field=models.ForeignKey(to='video.Video'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sequence',
            name='vid',
            field=models.ForeignKey(to='video.Video'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='video',
            name='pub_date',
            field=models.DateTimeField(auto_now=True),
            preserve_default=True,
        ),
    ]
