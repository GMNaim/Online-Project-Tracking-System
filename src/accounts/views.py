import re

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect

from adminusers.models import Client, Module, Task
from teams.models import Team
from .decorators import has_access
from .models import Department
from .models import User

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
@has_access(allowed_roles=['Super User', 'Admin', 'Employee', 'Department Head', 'Team Leader', 'Team Member'])
def dashboard(request):
    if request.user.is_authenticated:
        """"""
        is_super_user_or_admin = request.user.role.name == 'Admin' or request.user.role.name == 'Super User'
        is_department_head = request.user.role.name == 'Department Head'
        is_team_leader = request.user.role.name == 'Team Leader'
        is_team_member = request.user.role.name == 'Team Member'
        is_employee = request.user.role.name == 'Employee'

        """ ADMIN SUPER USER INFO """
        total_employee = User.objects.filter(is_active=True).count()
        total_department = Department.objects.exclude(id=16).filter(is_active=True).count()
        total_team = Team.objects.exclude(id=10).count()
        total_client = Client.objects.all().count()
        total_module_of_leader = Module.objects.filter(assigned_team=request.user.team_member, status__gte=2).count()
        total_task_of_member = Task.objects.filter(assigned_member=request.user).count()

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

        # total members in the team
        members_in_team = User.objects.filter(team_member__id=request.user.team_member.id).count()
        print('member in the team ', members_in_team)
        context = {'total_employee': total_employee,
                   'total_department': total_department,
                   'total_team': total_team,
                   'total_client': total_client,
                   'is_super_user_or_admin': is_super_user_or_admin,
                   'is_department_head': is_department_head,
                   'is_team_leader': is_team_leader,
                   'is_employee': is_employee,
                   'is_team_member': is_team_member,
                   'members_in_team': members_in_team,
                   'total_module_of_leader': total_module_of_leader,
                   'total_task_of_member': total_task_of_member}

        if is_super_user_or_admin:
            return render(request, 'adminusers/admin_dashboard.html', context)
        elif is_department_head:
            return render(request, 'departments/head_dashboard.html', context)
        elif is_team_leader:
            return render(request, 'teams/leader_dashboard.html', context)
        elif is_team_member or is_team_leader:
            return render(request, 'members/member_dashboard.html', context)
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
@has_access(allowed_roles=['Super User', 'Admin', 'Employee', 'Department Head', 'Team Leader', 'Team Member'])
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
