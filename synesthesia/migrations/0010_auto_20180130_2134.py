# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-01-30 21:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('synesthesia', '0009_auto_20180110_2223'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(default='', max_length=255),
        ),
    ]