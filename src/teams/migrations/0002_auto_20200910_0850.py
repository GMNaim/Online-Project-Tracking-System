# Generated by Django 3.1.1 on 2020-09-10 02:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('teams', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='team',
            name='leader',
        ),
        migrations.AddField(
            model_name='team',
            name='leader',
            field=models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.PROTECT, related_name='team_leader_user', to='accounts.user', unique=True),
            preserve_default=False,
        ),
    ]
