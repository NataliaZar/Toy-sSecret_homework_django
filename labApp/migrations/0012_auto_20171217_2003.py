# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-17 17:03
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('labApp', '0011_auto_20171217_1417'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='img',
        ),
        migrations.RemoveField(
            model_name='prodact',
            name='img',
        ),
    ]
