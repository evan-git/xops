# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-10 14:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmdb', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='asset',
            name='cpu_count',
        ),
        migrations.RemoveField(
            model_name='asset',
            name='platform',
        ),
        migrations.AddField(
            model_name='asset',
            name='kernel',
            field=models.CharField(blank=True, max_length=128, null=True, verbose_name='内核'),
        ),
        migrations.AddField(
            model_name='asset',
            name='kernel_version',
            field=models.CharField(blank=True, max_length=128, null=True, verbose_name='内核版本'),
        ),
    ]
