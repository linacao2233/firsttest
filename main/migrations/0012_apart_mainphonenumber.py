# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-30 19:03
from __future__ import unicode_literals

from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_auto_20170830_2046'),
    ]

    operations = [
        migrations.AddField(
            model_name='apart',
            name='mainphonenumber',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True),
        ),
    ]