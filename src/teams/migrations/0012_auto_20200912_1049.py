# Generated by Django 3.1.1 on 2020-09-12 04:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0011_auto_20200912_1042'),
    ]

    operations = [
        migrations.AlterField(
            model_name='membership',
            name='team',
            field=models.ForeignKey(default=10, on_delete=django.db.models.deletion.DO_NOTHING, to='teams.team'),
        ),
    ]