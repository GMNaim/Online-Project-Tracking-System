from django.db import models

from accounts.models import User
from departments.models import Department


class Team(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True, default='')
    department = models.ForeignKey(Department, on_delete=models.PROTECT, blank=False)
    members = models.ManyToManyField(User, through='Membership')

    def __str__(self):
        return self.name


class Membership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    date_joined = models.DateField(auto_now_add=True)
    is_leader = models.BooleanField(default=False)
    is_member = models.BooleanField(default=True)

    def __str__(self):
        return self.user.get_full_name() + '-->' + self.team.name

