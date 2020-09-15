from django.db import models
from django.utils import timezone

from departments.models import Department


class Client(models.Model):

    GENDER = (
        (1, 'Male'),
        (2, 'Female'),
        (3, 'Other'),
    )
    name = models.CharField(max_length=100)
    client_id = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    phone = models.CharField(max_length=13)
    company_name = models.CharField(max_length=150, default='N/A')
    address = models.TextField(null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='users/client/%Y/%m/%d/', blank=True, null=True,
                                        default='users/default_user.png')
    date_added = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Project(models.Model):
    PROJECT_STATUS = (
        (1, 'New'),
        (2, 'Assigned'),
        (3, 'Running'),
        (4, 'Completed')
    )

    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255)
    description = models.TextField()
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.SET_DEFAULT, default=16)  # 16=Not Assigned dep..
    status = models.IntegerField(choices=PROJECT_STATUS, default=1)
    department_head_notified = models.BooleanField(default=False)
    delivery_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    modified_at = models.DateTimeField(auto_now=True)

