# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-05 13:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_apart_mainphonenumber'),
    ]

    operations = [
        migrations.AddField(
            model_name='apart',
            name='pricehigh',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='apart',
            name='pricelow',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
