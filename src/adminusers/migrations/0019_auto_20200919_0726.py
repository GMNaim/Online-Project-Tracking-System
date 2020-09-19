# Generated by Django 3.1.1 on 2020-09-19 01:26

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminusers', '0018_auto_20200919_0716'),
    ]

    operations = [
        migrations.AddField(
            model_name='module',
            name='completed_at',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='project',
            name='completed_at',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='submittedtoqatask',
            name='bug',
            field=models.TextField(default='No Bug'),
        ),
        migrations.AddField(
            model_name='submittedtoqatask',
            name='is_verified',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='submittedtoqatask',
            name='verified_at',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='task',
            name='completed_at',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='submittedtoqatask',
            name='submitted_at',
            field=models.DateField(default=datetime.datetime(2020, 9, 19, 7, 26, 58, 426178)),
        ),
    ]
