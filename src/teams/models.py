from django.db import models

from departments.models import Department


class Team(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True, default='')
    department = models.ForeignKey(Department, on_delete=models.PROTECT, blank=False)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    # didn't use these methods but can use.... if get time then refactor with existing team list code.
    def get_total_member(self):
        member = ''
        try:
            mem_list = []
            from accounts.models import User
            memberlist = User.objects.filter(team_member_id=self.id)
            for m in memberlist:
                mem_list.append(m.username)
            member = ', '.join(mem_list)
        except:
            member = ''
        return member

    def get_team_leader(self):
        team_leader = ''
        try:
            from accounts.models import User
            team_leader = User.objects.filter(is_team_leader=True).get(team_member_id=self.id)

        except:
            team_leader = ''
        return team_leader