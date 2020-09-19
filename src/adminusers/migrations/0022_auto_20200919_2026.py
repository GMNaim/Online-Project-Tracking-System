# Generated by Django 3.1.1 on 2020-09-19 14:26

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminusers', '0021_auto_20200919_1950'),
    ]

    operations = [
        migrations.AddField(
            model_name='submittedtoqatask',
            name='assigned_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='submittedtoqatask',
            name='has_bug',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='submittedtoqatask',
            name='status',
            field=models.IntegerField(choices=[(1, 'New'), (2, 'Assigned'), (3, 'Running'), (4, 'Verified')], default=1),
        ),
        migrations.AlterField(
            model_name='submittedtoqatask',
            name='submitted_at',
            field=models.DateField(default=datetime.datetime(2020, 9, 19, 20, 26, 26, 446042)),
        ),
    ]
