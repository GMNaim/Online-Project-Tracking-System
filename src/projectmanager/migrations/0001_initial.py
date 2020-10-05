# Generated by Django 3.1.1 on 2020-10-03 14:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import projectmanager.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('teams', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('departments', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('client_id', models.CharField(max_length=100, unique=True)),
                ('email', models.EmailField(max_length=100, unique=True)),
                ('phone', models.CharField(max_length=13)),
                ('company_name', models.CharField(default='N/A', max_length=150)),
                ('address', models.TextField(blank=True, null=True)),
                ('comment', models.TextField(blank=True, null=True)),
                ('profile_picture', models.ImageField(blank=True, default='users/default_user.png', null=True, upload_to='users/client/%Y/%m/%d/')),
                ('date_added', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Module',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('status', models.IntegerField(choices=[(1, 'New'), (2, 'Assigned'), (3, 'Running'), (4, 'Completed')], default=1)),
                ('team_leader_notified', models.BooleanField(default=False)),
                ('submission_date', models.DateField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('assigned_at', models.DateTimeField(blank=True, default=None, null=True)),
                ('completed_at', models.DateTimeField(blank=True, default=None, null=True)),
                ('assigned_team', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='teams.team')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('code', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('status', models.IntegerField(choices=[(1, 'New'), (2, 'Assigned'), (3, 'Running'), (4, 'Completed')], default=1)),
                ('department_head_notified', models.BooleanField(default=False)),
                ('delivery_date', models.DateField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('assigned_at', models.DateTimeField(blank=True, default=None, null=True)),
                ('completed_at', models.DateTimeField(blank=True, default=None, null=True)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projectmanager.client')),
                ('department', models.ForeignKey(default=16, on_delete=django.db.models.deletion.SET_DEFAULT, to='departments.department')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='SubmittedToQATask',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('submitted_file', models.FileField(blank=True, null=True, upload_to=projectmanager.models.user_directory_path)),
                ('tester_notified', models.BooleanField(default=False)),
                ('bug', models.TextField(default='No Bug')),
                ('has_bug', models.BooleanField(default=False)),
                ('status', models.IntegerField(choices=[(1, 'New'), (2, 'Running'), (3, 'Need Modification'), (4, 'Verified')], default=1)),
                ('submission_date', models.DateField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('assigned_at', models.DateTimeField(blank=True, null=True)),
                ('verified_at', models.DateTimeField(blank=True, default=None, null=True)),
                ('is_verified', models.BooleanField(default=False)),
                ('assigned_member', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('status', models.IntegerField(choices=[(1, 'New'), (2, 'Assigned'), (3, 'Running'), (4, 'Submitted to Tester'), (5, 'Need Modification'), (6, 'Test Passed'), (7, 'Completed')], default=1)),
                ('team_member_notified', models.BooleanField(default=False)),
                ('submission_date', models.DateField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('assigned_at', models.DateTimeField(blank=True, default=None, null=True)),
                ('is_send_tester', models.BooleanField(default=False)),
                ('submitted_to_tester_at', models.DateTimeField(blank=True, default=None, null=True)),
                ('completed_at', models.DateTimeField(blank=True, default=None, null=True)),
                ('is_send_to_leader', models.BooleanField(default=False)),
                ('assigned_member', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('module', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='projectmanager.module')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='TaskHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(default='', max_length=255)),
                ('description', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('module', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='projectmanager.module')),
                ('project', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='projectmanager.project')),
                ('submitted_task', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='projectmanager.submittedtoqatask')),
                ('task', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='projectmanager.task')),
            ],
        ),
        migrations.AddField(
            model_name='submittedtoqatask',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='projectmanager.task'),
        ),
        migrations.AddField(
            model_name='module',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='projectmanager.project'),
        ),
    ]
