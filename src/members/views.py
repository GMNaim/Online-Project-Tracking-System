# members/views.py

from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect, get_object_or_404

from accounts.decorators import has_access
from accounts.models import User, Role
from adminusers.models import Module, Task
from departments.models import Department
from teams.models import Team


# Role Names
role_super_user = 'Super User'
role_admin = 'Admin'
role_department_head = 'Department Head'
role_team_leader = 'Team Leader'
role_team_member = 'Team Member'
role_employee = 'Employee'

default_password = 'test123'  # default pass
# getting user group
group_super_user = Group.objects.get(name__iexact=role_super_user)
group_admin = Group.objects.get(name__iexact=role_admin)
group_department_head = Group.objects.get(name__iexact=role_department_head)
group_team_leader = Group.objects.get(name__iexact=role_team_leader)
group_team_member = Group.objects.get(name__iexact=role_team_member)
group_employee = Group.objects.get(name__iexact=role_employee)


@login_required(login_url='login')
@has_access(allowed_roles=[role_team_member])
def member_all_task(request):
    # user_notification_item = Module.objects.filter(
    #     assigned_team__team_member_user__username__iexact=request.user.username, status__gte=2)
    # print(user_notification_item, ' = user_notification_item')
    assigned_tasks_list_to_member = Task.objects.filter(assigned_member=request.user,
                                                        status__gte=2).order_by('status', '-assigned_at')
    print('assigned_tasks_list_to_member == ', assigned_tasks_list_to_member)
    """ CHANGING THE NOTIFICATION COUNT TO ZERO """
    current_user = User.objects.get(id=request.user.id)
    current_user.notification_count = 0
    current_user.save()

    """ LIST OF NOTIFICATION ITEMS """
    user_notification_item = Task.objects.filter(assigned_member=request.user, status=2).order_by(
        'status', '-assigned_at')
    print('user_notification_item: -- ', user_notification_item)
    if current_user.notification_count == 0:
        user_notification_item = None

    context = {'assigned_tasks_list_to_member': assigned_tasks_list_to_member,
               'user_notification_item': user_notification_item}
    return render(request, 'members/member_all_task.html', context)



@login_required(login_url='login')
@has_access(allowed_roles=[role_team_member])
def member_task_details(request, task_id):
    if request.user.is_authenticated:
        # user_notification_item = Project.objects.filter(department_id=request.user.department.id, status=2)
        selected_task = get_object_or_404(Task, id=task_id)
        selected_task.team_member_notified = True
        selected_task.save()
        module_of_the_task = selected_task.module   # getting the module of the task
        print(module_of_the_task)
        #  If member see details of the task then team_member_notified will be true and module's status will be 3
        if selected_task.team_member_notified:
            module_of_the_task.status = 3  # if any task then status will be 3 means running
            module_of_the_task.save()
        context = {'selected_task': selected_task}
        return render(request, 'members/member_task_details.html', context)
