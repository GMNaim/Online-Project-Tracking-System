import re

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect

from projectmanager.models import Client, Module, Task, SubmittedToQATask, Project
from teams.models import Team
from .decorators import has_access, has_access_dashboard
from .models import Department
from .models import User

# Role Names
role_super_user = 'Super User'
role_pm = 'Project Manager'
role_department_head = 'Department Head'
role_team_leader = 'Team Leader'
role_team_member = 'Team Member'
role_employee = 'Employee'
role_tester = 'Tester'

default_password = 'test123'  # default pass
# getting user group
group_super_user = Group.objects.get(name__iexact=role_super_user)
group_pm = Group.objects.get(name__iexact=role_pm)
group_department_head = Group.objects.get(name__iexact=role_department_head)
group_team_leader = Group.objects.get(name__iexact=role_team_leader)
group_team_member = Group.objects.get(name__iexact=role_team_member)
group_employee = Group.objects.get(name__iexact=role_employee)
group_tester = Group.objects.get(name__iexact=role_tester)


@login_required(login_url='login')
@has_access_dashboard(
    allowed_roles=[role_super_user, role_pm, role_team_leader, role_team_member, role_tester, role_employee,
                   role_department_head])
def dashboard(request):
    if request.user.is_authenticated:
        """"""
        is_super_user_or_pm = request.user.role.name == role_pm or request.user.role.name == role_super_user
        is_department_head = request.user.role.name == role_department_head
        is_team_leader = request.user.role.name == role_team_leader
        is_team_member = request.user.role.name == role_team_member
        is_employee = request.user.role.name == role_employee
        is_tester = request.user.role.name == role_tester
        print('dashboard testing================')
        """ Project Manager SUPER USER INFO """


        # task count of member
        total_task_of_member = Task.objects.filter(assigned_member=request.user, status__gte=2).count()
        completed_task_of_member = Task.objects.filter(assigned_member=request.user, status=7).count()
        # Task count of tester
        total_task_of_tester = SubmittedToQATask.objects.filter(assigned_member=request.user).count()
        running_tasks_count_of_tester = SubmittedToQATask.objects.filter(assigned_member=request.user, status=2).count()
        completed_tasks_count_of_tester = SubmittedToQATask.objects.filter(assigned_member=request.user,
                                                                           status__in=[3, 4]).count()

        # """ DEPARTMENT INFO """
        # total_team_in_department = Team.objects.filter(department__name__iexact=request.user.department.name).count()

        # """ NOTIFICATIONS SETTING """
        # user_notification_count = Project.objects.filter(department_id=request.user.department.id, status=2).count()  # all projects that are assigned to the head

        # """ LIST OF NOTIFICATION ITEMS """
        # user_notification_item = Project.objects.filter(department_id=request.user.department.id, status=2)

        """CHANGE notification_count value"""
        # project_assigned_dep_head = User.objects.get(department_id=request.user.department.id,
        #                                              role__name__iexact='Department Head')
        # # print('444 req.$$$$$$$$$$$$$$$$$$$$', project_assigned_dep_head.notification_count)
        # if request.method == "POST":
        #     project_assigned_dep_head.notification_count = 0
        # print('post req.$$$$$$$$$$$$$$$$$$$$', project_assigned_dep_head.notification_count)


        context = {'is_super_user_or_pm': is_super_user_or_pm,
                   'is_department_head': is_department_head,
                   'is_team_leader': is_team_leader,
                   'is_employee': is_employee,
                   'is_team_member': is_team_member,
                   'is_tester': is_tester,

                   'total_task_of_member': total_task_of_member,
                   'completed_task_of_member': completed_task_of_member,

                   'total_task_of_tester': total_task_of_tester,
                   'running_tasks_count_of_tester': running_tasks_count_of_tester,
                   'completed_tasks_count_of_tester': completed_tasks_count_of_tester,}

        if is_super_user_or_pm:
            total_projects = Project.objects.all().count()
            completed_project = Project.objects.filter(status=4).count()
            total_employee = User.objects.filter(is_active=True).exclude(role__name__iexact=role_super_user).count()
            total_department = Department.objects.exclude(id=16).filter(is_active=True).count()
            total_team = Team.objects.exclude(id=10).count()
            total_client = Client.objects.all().count()

            context['total_projects'] = total_projects
            context['completed_project'] = completed_project
            context['total_employee'] = total_employee
            context['total_department'] = total_department
            context['total_team'] = total_team
            context['total_client'] = total_client

            return render(request, 'projectmanager/pm_dashboard.html', context)


        elif is_department_head:
            total_project_of_department_head = Project.objects.filter(department=request.user.department,
                                                                      status__gt=1).count()
            running_project_of_department_head = Project.objects.filter(department=request.user.department,
                                                                        status=3).count()
            completed_project_of_department_head = Project.objects.filter(department=request.user.department,
                                                                          status=4).count()
            total_team = Team.objects.filter(department=request.user.department).count()
            context['total_project_of_department_head'] = total_project_of_department_head
            context['completed_project_of_department_head'] = completed_project_of_department_head
            context['running_project_of_department_head'] = running_project_of_department_head
            context['total_team'] = total_team

            return render(request, 'departments/head_dashboard.html', context)


        elif is_team_leader:
            # total members in the team
            members_in_team = User.objects.filter(team_member__id=request.user.team_member.id).count()
            # Leader
            total_module_of_leader = Module.objects.filter(assigned_team=request.user.team_member, status__gte=2).count()
            running_module_of_leader = Module.objects.filter(assigned_team=request.user.team_member, status=3).count()
            completed_module_of_leader = Module.objects.filter(assigned_team=request.user.team_member, status=4).count()

            context['members_in_team'] = members_in_team
            context['total_module_of_leader'] = total_module_of_leader
            context['running_module_of_leader'] = running_module_of_leader
            context['completed_module_of_leader'] = completed_module_of_leader
            return render(request, 'teams/leader_dashboard.html', context)


        elif is_team_member or is_team_leader:
            return render(request, 'members/member_dashboard.html', context)


        elif is_tester:
            return render(request, 'members/tester_dashboard.html', context)


        elif is_employee:
            return render(request, 'teams/leader_dashboard.html', context)


def registration_view(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name', '')
        username = str(request.POST.get('username')).strip()
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        print(first_name, last_name, username, email, password1, password2)

        context = {'first_name': first_name, 'last_name': last_name, "username": username,
                   'email': email}

        # Validating the information
        employee_registration_error_link = 'accounts/registration.html'
        if username.strip() == "":
            messages.warning(request, 'You must have to provide a username')
            return render(request, employee_registration_error_link, context)

        elif User.objects.filter(username=username).exists():
            messages.warning(request, f"Username {username} is already exists!")
            return render(request, employee_registration_error_link, context)

        elif re.match(r"^[a-zA-Z0-9_.-]+$", username) is None:
            messages.warning(request, f"Username {username} is not valid! Please provide a valid username")
            return render(request, employee_registration_error_link, context)

        elif email.strip() == "":
            messages.warning(request, 'You must have to provide a email!')
            return render(request, employee_registration_error_link, context)

        elif User.objects.filter(email=email).exists():
            messages.warning(request, f"Email {email} is already exists!")
            return render(request, employee_registration_error_link, context)

        elif first_name.strip() == "":
            messages.warning(request, f"Please Provide first name!")
            return render(request, employee_registration_error_link, context)

        elif last_name.strip() == "":
            messages.warning(request, f"Please Provide last name!")
            return render(request, employee_registration_error_link, context)
        elif password1 != password2:
            messages.warning(request, "Your password is not matched")
            return render(request, employee_registration_error_link, context)

        else:
            # Adding user in the database
            try:
                user = User()
                user.first_name = first_name
                user.last_name = last_name
                user.username = username
                user.email = email
                user.save()
                user.set_password(password1)
                user.save()
                # Adding employee to employee group.
                group = Group.objects.get(name__iexact='Employee')
                print(group, '--======================--')
                group.user_set.add(user)

                messages.success(request,
                                 f"Hi {first_name} {last_name}, you have successfully registered. Please sign in now.")
                return redirect('login')

            except Exception as e:
                print(e, 'exception -----------=========================================!!!!!!!!!!!!!!!!!!!')
                messages.error(request, f"Error: {e}")
                return render(request, employee_registration_error_link)

    return render(request, 'accounts/registration.html')


def login_view(request):
    """     Login      """
    if request.method == "POST":  # If method=POST then request is valid otherwise not
        employee_username = request.POST['username']  # Collecting employee id
        password = request.POST['password']  # Collecting password
        user = authenticate(username=employee_username,
                            password=password)  # If user is valid then authenticte otherwise not
        if user is not None:
            print('testing-------------------------')
            login(request, user)  # If valid user then login
            return redirect('dashboard')
        else:  # If username / password is wrong
            messages.error(request, 'Invalid Credentials!')
            return render(request, 'accounts/login.html')
    else:
        if request.user.is_authenticated:
            return redirect('dashboard')
        return render(request, 'accounts/login.html')


@login_required(login_url='login')
@has_access(
    allowed_roles=[role_pm, role_employee, role_department_head, role_team_member, role_team_leader, role_tester,
                   role_super_user])
def logout_view(request):
    """ Logout for all users """
    logout(request)
    return redirect(login_view)


def forgot_password_view(request):
    return render(request, 'accounts/forgotPass01.html')


def security_code_view(request):
    return render(request)


def change_password_view(request):
    render(request, 'accounts/changePassword.html')
