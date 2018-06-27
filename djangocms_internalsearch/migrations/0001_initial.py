# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-27 13:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='InternalSearch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('query', models.CharField(default='*', max_length=255)),
            ],
            options={
                'verbose_name': 'Search',
                'verbose_name_plural': 'Searches',
                'db_table': 'djangocms_internalsearch',
            },
        ),
    ]
