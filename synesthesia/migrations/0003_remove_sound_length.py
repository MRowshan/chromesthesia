# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-27 21:13
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('synesthesia', '0002_auto_20171227_1630'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sound',
            name='length',
        ),
    ]
