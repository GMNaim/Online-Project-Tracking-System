# Generated by Django 3.1.1 on 2020-09-15 04:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('departments', '0002_department_description'),
        ('adminusers', '0004_remove_client_gender'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('code', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('status', models.IntegerField(choices=[(1, 'New'), (2, 'Assigned'), (3, 'Running'), (4, 'Completed')], default=1)),
                ('department_head_notified', models.BooleanField(default=False)),
                ('delivery_date', models.DateTimeField(help_text='When should the project deliver to client')),
                ('created_at', models.DateTimeField(editable=False)),
                ('modified_at', models.DateTimeField()),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adminusers.client')),
                ('department', models.ForeignKey(default=16, on_delete=django.db.models.deletion.SET_DEFAULT, to='departments.department')),
            ],
        ),
    ]
