# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-16 22:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('labApp', '0006_auto_20171216_1311'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='number',
            field=models.IntegerField(default=1, verbose_name='Количетво'),
        ),
    ]
