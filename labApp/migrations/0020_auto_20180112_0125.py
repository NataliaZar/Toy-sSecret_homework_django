# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-01-11 22:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('labApp', '0019_auto_20180112_0008'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_price',
            field=models.IntegerField(default=0, verbose_name='Стоимость заказа'),
        ),
        migrations.AlterField(
            model_name='prodact',
            name='price',
            field=models.IntegerField(max_length=10, verbose_name='Цена'),
        ),
    ]