# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-04-19 09:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=30)),
                ('project_name', models.CharField(max_length=30)),
                ('start_time', models.TimeField()),
                ('last_modified_time', models.TimeField()),
                ('status', models.CharField(max_length=4)),
                ('major_files', models.TextField()),
                ('minor_files', models.TextField()),
                ('generated_files', models.TextField()),
            ],
        ),
    ]