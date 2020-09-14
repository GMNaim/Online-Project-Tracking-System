from django.db import models

from departments.models import Department


class Team(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True, default='')
    department = models.ForeignKey(Department, on_delete=models.PROTECT, blank=False)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name
