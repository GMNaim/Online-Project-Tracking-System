# Generated by Django 3.1.1 on 2020-10-07 11:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projectmanager', '0004_auto_20201005_0944'),
    ]

    operations = [
        migrations.AddField(
            model_name='taskhistory',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
