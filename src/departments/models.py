from django.db import models


class Department(models.Model):
    name = models.CharField(max_length=30, unique=True)
    is_active = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

