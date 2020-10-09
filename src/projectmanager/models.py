from django.db import models
from django.utils import timezone
from datetime import datetime

from accounts.models import User
from departments.models import Department
from teams.models import Team


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
    assigned_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.SET_DEFAULT, default=16)  # 16=Not Assigned dep..
    status = models.IntegerField(choices=PROJECT_STATUS, default=1)
    department_head_notified = models.BooleanField(default=False)
    delivery_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    modified_at = models.DateTimeField(auto_now=True)
    assigned_at = models.DateTimeField(default=None, null=True, blank=True)
    completed_at = models.DateTimeField(default=None, null=True, blank=True)
    progress = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    def get_day_left_to_submit(self):
        # date_obj = datetime.strptime(self.submission_date, '%Y-%m-%d')  # converting string date to date obj
        # submission_date_obj = date_obj.date()  # datetime obj to save in model
        day_left = (self.delivery_date - datetime.today().date()).days
        if day_left < 0:
            return 0
        else:
            return day_left

    class Meta:
        ordering = ['-created_at']


class Module(models.Model):
    MODULE_STATUS = (
        (1, 'New'),
        (2, 'Assigned'),
        (3, 'Running'),
        (4, 'Completed')
    )
    from teams.models import Team
    name = models.CharField(max_length=100)
    description = models.TextField()
    assigned_team = models.ForeignKey(Team, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    status = models.IntegerField(choices=MODULE_STATUS, default=1)
    team_leader_notified = models.BooleanField(default=False)
    submission_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    modified_at = models.DateTimeField(auto_now=True)
    assigned_at = models.DateTimeField(default=None, null=True, blank=True)
    completed_at = models.DateTimeField(default=None, null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    progress = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    def get_day_left_to_submit(self):
        # date_obj = datetime.strptime(self.submission_date, '%Y-%m-%d')  # converting string date to date obj
        # submission_date_obj = date_obj.date()  # datetime obj to save in model
        day_left = (self.submission_date - datetime.today().date()).days
        if day_left < 0:
            return 0
        else:
            return day_left

    class Meta:
        ordering = ['-created_at']


class Task(models.Model):
    TASK_STATUS = (
        (1, 'New'),
        (2, 'Assigned'),
        (3, 'Running'),
        (4, 'Submitted to Tester'),
        (5, 'Need Modification'),
        (6, 'Test Passed'),
        (7, 'Completed')
    )
    name = models.CharField(max_length=100)
    description = models.TextField()
    assigned_member = models.ForeignKey(User, on_delete=models.CASCADE)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    status = models.IntegerField(choices=TASK_STATUS, default=1)
    team_member_notified = models.BooleanField(default=False)
    submission_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    modified_at = models.DateTimeField(auto_now=True)
    assigned_at = models.DateTimeField(default=None, null=True, blank=True)
    is_send_tester = models.BooleanField(default=False)
    submitted_to_tester_at = models.DateTimeField(default=None, null=True, blank=True)
    completed_at = models.DateTimeField(default=None, null=True, blank=True)
    is_send_to_leader = models.BooleanField(default=False)
    progress = models.IntegerField(default=0)

    def get_task_progress(self):
        if self.status == 1:
            self.progress = 0
            self.save()
        elif self.status == 2:
            self.progress = 10
            self.save()
        elif self.status == 3:
            self.progress = 50
            self.save()
        elif self.status == 4:
            self.progress = 80
            self.save()
        elif self.status == 5:
            self.progress = 70
            self.save()
        elif self.status == 6:
            self.progress = 95
            self.save()
        elif self.status == 7:
            self.progress = 100
            self.save()
        return self.progress


    def __str__(self):
        return self.name

    def get_day_left_to_submit(self):
        # date_obj = datetime.strptime(self.submission_date, '%Y-%m-%d')  # converting string date to date obj
        # submission_date_obj = date_obj.date()  # datetime obj to save in model
        day_left = (self.submission_date - datetime.today().date()).days
        if day_left < 0:
            return 0
        else:
            return day_left

    def get_tester_of_the_task(self):
        submitted_task_against_this_task = self.submittedtoqatask_set.filter(task=self).last()  #  as last submitted task
        return submitted_task_against_this_task.assigned_member

    class Meta:
        ordering = ['-created_at']


def user_directory_path(instance, filename):
    """To save the file under each user folder"""
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'submitted_task_files/user_{0}/{1}'.format(instance, filename)


class SubmittedToQATask(models.Model):
    TASK_STATUS = (
        (1, 'New'),
        (2, 'Running'),
        (3, 'Need Modification'),
        (4, 'Verified'),
    )
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    description = models.TextField()
    submitted_file = models.FileField(upload_to=user_directory_path, null=True, blank=True)
    tester_notified = models.BooleanField(default=False)
    assigned_member = models.ForeignKey(User, on_delete=models.CASCADE)
    bug = models.TextField(default='No Bug')
    has_bug = models.BooleanField(default=False)
    status = models.IntegerField(choices=TASK_STATUS, default=1)
    submission_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    modified_at = models.DateTimeField(auto_now=True)
    assigned_at = models.DateTimeField(null=True, blank=True)
    verified_at = models.DateTimeField(default=None, null=True, blank=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.task.name

    class Meta:
        ordering = ['-created_at']


class TaskHistory(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)
    module = models.ForeignKey(Module, on_delete=models.CASCADE, null=True, blank=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, null=True, blank=True)
    submitted_task = models.ForeignKey(SubmittedToQATask, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=255, default='')
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    modified_at = models.DateTimeField(auto_now=True)

    # def __str__(self):
    #     if self.project != '':
    #         return self.project.name
    #     elif self.module != "":
    #         return self.module.name
    #     elif self.task != "":
    #         return self.task.name
