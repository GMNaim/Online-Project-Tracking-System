from django.db import models

# from teams.models import Team


class Department(models.Model):
    name = models.CharField(max_length=30, unique=True)
    is_active = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    description = models.TextField(blank=True, null=True, default='')
    notification = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    # def get_department_info(self):
    #     from accounts.models import User
    #     user = User.objects.all()
    #     return user.employee_department.filter(name='Department Head')

    def get_department_info(self):
        from accounts.models import User
        department_head_name = None
        try:
            department_head_name = User.objects.get(role__name__iexact='Department Head', department__name__iexact=self.name)
        except:
            department_head_name = None
        return department_head_name

    def get_total_employee(self):
        from accounts.models import User
        total_employee = 0
        try:
            total_employee = User.objects.filter(department=self).count()
        except:
            total_employee = 0
        return total_employee

    def get_team_count(self):
        from teams.models import Team
        total_team = 0
        try:
            total_team = Team.objects.filter(department_id=self.id).count()
        except:
            total_team = 0
        return total_team

    def get_total_project(self):
        from projectmanager.models import Project
        total_project = 0
        try:
            total_project = Project.objects.filter(department_id=self.id).count()
        except:
            total_project = 0
        return total_project

    # def get_total_department(self):
    #     return self.objects.filter(is_active=True).count()

