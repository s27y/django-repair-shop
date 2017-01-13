# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-28 16:01
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('repairs', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='History',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('comment', models.CharField(max_length=500)),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='repairs.Job')),
            ],
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status_text', models.CharField(max_length=100)),
                ('index', models.FloatField()),
            ],
        ),
        migrations.AddField(
            model_name='history',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='repairs.Status'),
        ),
    ]
