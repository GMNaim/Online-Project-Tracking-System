# Generated by Django 3.1.1 on 2020-09-10 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0003_auto_20200910_0914'),
    ]

    operations = [
        migrations.AddField(
            model_name='teammember',
            name='is_leader',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='team',
            name='name',
            field=models.CharField(blank=True, default='', max_length=100, null=True),
        ),
    ]