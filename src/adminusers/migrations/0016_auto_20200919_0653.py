# Generated by Django 3.1.1 on 2020-09-19 00:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminusers', '0015_auto_20200918_1517'),
    ]

    operations = [
        migrations.AlterField(
            model_name='module',
            name='status',
            field=models.IntegerField(choices=[(1, 'New'), (2, 'Assigned'), (3, 'Running'), (4, 'Submitted to QA'), (5, 'Completed')], default=1),
        ),
    ]
