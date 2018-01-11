# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-06 06:09
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Asset',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hostname', models.CharField(blank=True, max_length=128, null=True, verbose_name='主机名')),
                ('asset_type', models.PositiveSmallIntegerField(choices=[(0, '物理机'), (1, '虚拟机'), (2, '交换机'), (3, '路由器'), (4, '其它设备')], default=1, verbose_name='资产类型')),
                ('remote_card_ip', models.CharField(blank=True, max_length=16, null=True, verbose_name='远程管理卡地址')),
                ('vendor', models.CharField(blank=True, max_length=64, null=True, verbose_name='制造商')),
                ('sn', models.CharField(blank=True, max_length=128, null=True, verbose_name='Serial number')),
                ('cpu_model', models.CharField(blank=True, max_length=64, null=True, verbose_name='CPU model')),
                ('cpu_count', models.IntegerField(null=True, verbose_name='CPU count')),
                ('cpu_cores', models.IntegerField(null=True, verbose_name='CPU cores')),
                ('memory', models.CharField(blank=True, max_length=64, null=True, verbose_name='内存(GB)')),
                ('disk_total', models.CharField(blank=True, max_length=1024, null=True, verbose_name='磁盘容量')),
                ('disk_info', models.CharField(blank=True, max_length=1024, null=True, verbose_name='磁盘信息')),
                ('platform', models.CharField(blank=True, max_length=128, null=True, verbose_name='Platform')),
                ('os', models.CharField(blank=True, max_length=128, null=True, verbose_name='OS')),
                ('os_version', models.CharField(blank=True, max_length=16, null=True, verbose_name='OS version')),
                ('os_arch', models.CharField(blank=True, max_length=16, null=True, verbose_name='OS arch')),
                ('create_date', models.DateTimeField(auto_now=True, verbose_name='添加时间')),
                ('update_date', models.DateTimeField(blank=True, null=True, verbose_name='更新时间')),
                ('comment', models.TextField(blank=True, default='', max_length=128, verbose_name='备注')),
            ],
            options={
                'verbose_name': '资产',
                'verbose_name_plural': '资产',
            },
        ),
        migrations.CreateModel(
            name='AssetGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='资产分组')),
                ('common', models.CharField(max_length=200, verbose_name='分组描述')),
            ],
            options={
                'verbose_name': '资产分组',
                'verbose_name_plural': '资产分组',
            },
        ),
        migrations.CreateModel(
            name='Idc',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='机房名称')),
                ('address', models.CharField(max_length=200, verbose_name='机房地址')),
                ('contact_name', models.CharField(max_length=20, verbose_name='联系人姓名')),
                ('contact_phone', models.PositiveIntegerField(verbose_name='联系人电话')),
            ],
            options={
                'verbose_name': '机房',
                'verbose_name_plural': '机房',
            },
        ),
        migrations.CreateModel(
            name='IpAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip_address', models.CharField(max_length=20, verbose_name='IP地址')),
                ('is_vip', models.BooleanField(default=False, verbose_name='是否是vip')),
            ],
            options={
                'verbose_name': 'IP地址',
                'ordering': ['-ip_address'],
                'verbose_name_plural': 'IP地址',
            },
        ),
        migrations.CreateModel(
            name='Network',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usage', models.CharField(max_length=100, verbose_name='用途')),
                ('subnet', models.CharField(max_length=20, verbose_name='子网')),
                ('netmask', models.PositiveSmallIntegerField(verbose_name='网络掩码')),
                ('date', models.DateTimeField(auto_now=True, verbose_name='添加时间')),
                ('idc', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cmdb.Idc')),
            ],
            options={
                'verbose_name': '网络',
                'verbose_name_plural': '网络',
            },
        ),
        migrations.AddField(
            model_name='ipaddress',
            name='network',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cmdb.Network'),
        ),
        migrations.AddField(
            model_name='asset',
            name='group',
            field=models.ManyToManyField(to='cmdb.AssetGroup', verbose_name='资产分组'),
        ),
        migrations.AddField(
            model_name='asset',
            name='ip',
            field=models.ManyToManyField(to='cmdb.IpAddress', verbose_name='IP 地址'),
        ),
    ]
