# Generated by Django 3.1.1 on 2020-10-03 14:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('departments', '0001_initial'),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='department',
            field=models.ForeignKey(blank=True, default=16, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='employee_department', to='departments.department'),
        ),
    ]
