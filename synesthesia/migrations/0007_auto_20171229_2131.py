# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-29 21:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('synesthesia', '0006_user_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attemptone',
            name='userOne',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='attempttwo',
            name='userTwo',
            field=models.CharField(max_length=100),
        ),
    ]
