# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-28 06:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oauth', '0003_auto_20160628_0134'),
    ]

    operations = [
        migrations.AlterField(
            model_name='oauthtoken',
            name='expire_date',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
    ]