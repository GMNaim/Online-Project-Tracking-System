# Generated by Django 3.1.1 on 2020-10-05 02:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projectmanager', '0002_auto_20201003_2125'),
    ]

    operations = [
        migrations.AddField(
            model_name='module',
            name='is_completed',
            field=models.BooleanField(default=False),
        ),
    ]
