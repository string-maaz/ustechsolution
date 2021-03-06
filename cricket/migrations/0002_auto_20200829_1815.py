# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2020-08-29 18:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cricket', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='match_status',
            field=models.CharField(choices=[('1', 'Win'), ('2', 'Draw')], default='2', max_length=2, verbose_name='Match Status'),
        ),
        migrations.AlterField(
            model_name='team',
            name='club_state',
            field=models.CharField(blank=True, db_index=True, max_length=100, verbose_name='Club State'),
        ),
    ]
