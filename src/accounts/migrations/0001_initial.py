# Generated by Django 3.1.1 on 2020-10-03 14:24

import django.contrib.auth.models
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('departments', '0001_initial'),
        ('teams', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('middle_name', models.CharField(blank=True, max_length=50, null=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('username', models.CharField(max_length=50, unique=True, validators=[django.core.validators.RegexValidator(message='Username contains alphanumeric, underscore and period(.). Length: 4 to 50', regex='[-a-zA-Z0-9_.]{4,50}$')])),
                ('mobile_number', models.CharField(blank=True, default='', max_length=12, null=True)),
                ('gender', models.IntegerField(choices=[(1, 'Male'), (2, 'Female'), (3, 'Other')], default=1)),
                ('address', models.TextField(blank=True, null=True)),
                ('country', models.IntegerField(default=1)),
                ('profile_picture', models.ImageField(blank=True, default='users/default_user.png', null=True, upload_to='users/%Y/%m/%d/')),
                ('is_team_leader', models.BooleanField(default=False)),
                ('notification_count', models.IntegerField(default=0)),
                ('is_tester', models.BooleanField(default=False)),
                ('department', models.ForeignKey(blank=True, default=16, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='employee_department', to='departments.department')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('role', models.ForeignKey(default=6, on_delete=django.db.models.deletion.PROTECT, related_name='user_role', to='accounts.role')),
                ('team_member', models.ForeignKey(blank=True, default=10, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='team_member_user', to='teams.team')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
