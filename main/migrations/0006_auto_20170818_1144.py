# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-18 11:44
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20170818_1047'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='owner',
            new_name='created_by',
        ),
    ]