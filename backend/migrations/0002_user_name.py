# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-03 06:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='name',
            field=models.CharField(default='', max_length=16),
        ),
    ]