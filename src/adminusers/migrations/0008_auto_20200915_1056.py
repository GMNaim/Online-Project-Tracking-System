# Generated by Django 3.1.1 on 2020-09-15 04:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminusers', '0007_auto_20200915_1055'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='delivery_date',
            field=models.DateField(help_text='When should the project deliver to client'),
        ),
    ]
