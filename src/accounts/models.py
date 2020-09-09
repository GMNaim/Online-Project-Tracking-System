from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from departments.models import Department


class Role(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class User(AbstractUser):
    GENDER = (
        (1, 'Male'),
        (2, 'Female'),
        (3, 'Other'),
    )

    middle_name = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(unique=True, null=False, blank=False)
    username = models.CharField(max_length=50, unique=True, null=False, blank=False,
                                validators=[RegexValidator(
                                    regex='[-a-zA-Z0-9_.]{4,50}$',
                                    message='Username contains alphanumeric, underscore and period(.). Length: 4 to 50'
                                )])
    role = models.ForeignKey(
        Role, on_delete=models.PROTECT, null=False, blank=False, related_name='user_role', default=1)
    department = models.ForeignKey(Department, on_delete=models.PROTECT, null=True, blank=True,
                                   related_name='employee_department', default=1)
    mobile_number = models.CharField(max_length=12)
    gender = models.IntegerField(choices=GENDER, default=1)
    address = models.TextField(blank=True, null=True)
    country = models.IntegerField(default=1)
    profile_picture = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True, null=True,
                                        default='users/default_user.png')

    def get_full_name(self):
        if self.first_name is None:
            self.first_name = ''
        if self.middle_name is None:
            self.middle_name = ''
        if self.last_name is None:
            self.last_name = ''

        return f'{self.first_name} {self.middle_name} {self.last_name}'
