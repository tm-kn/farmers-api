# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-17 18:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('farmers', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='farmer',
            name='town',
            field=models.CharField(db_index=True, max_length=50, verbose_name='town'),
        ),
    ]