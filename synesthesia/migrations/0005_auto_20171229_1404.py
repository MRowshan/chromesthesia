# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-29 14:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('synesthesia', '0004_auto_20171229_0020'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='colour',
            name='id',
        ),
        migrations.RemoveField(
            model_name='sound',
            name='id',
        ),
        migrations.RemoveField(
            model_name='user',
            name='id',
        ),
        migrations.AddField(
            model_name='colour',
            name='colourID',
            field=models.IntegerField(default=0, primary_key=True, serialize=False),
        ),
        migrations.AddField(
            model_name='sound',
            name='soundID',
            field=models.IntegerField(default=0, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.CharField(max_length=100, primary_key=True, serialize=False),
        ),
    ]