import random
import re
from datetime import datetime

from departments.models import Department
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from opts import credentials
from projectmanager.models import Client, Module, Task, SubmittedToQATask, Project
from teams.models import Team

from .decorators import has_access, has_access_dashboard
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
        # print('dashboard testing================')
        """ Project Manager SUPER USER INFO """

        # task count of member
        # total_task_of_member = Task.objects.filter(assigned_member=request.user, status__gte=2).count()
        # completed_task_of_member = Task.objects.filter(assigned_member=request.user, status=7).count()
        # running_task_of_member = Task.objects.filter(assigned_member=request.user, status=3).count()
        # test_passed_task_of_member = Task.objects.filter(assigned_member=request.user, status=6).count()
        # submitted_to_tester_task_of_member = Task.objects.filter(assigned_member=request.user, status=4).count()
        # need_modification_task_of_member = Task.objects.filter(assigned_member=request.user, status=5).count()
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

                   'total_task_of_tester': total_task_of_tester,
                   'running_tasks_count_of_tester': running_tasks_count_of_tester,
                   'completed_tasks_count_of_tester': completed_tasks_count_of_tester, }

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
            total_module_of_leader = Module.objects.filter(assigned_team=request.user.team_member,
                                                           status__gte=2).count()
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
        # print(first_name, last_name, username, email, password1, password2)

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
                # print(group, '--======================--')
                group.user_set.add(user)

                messages.success(request,
                                 f"Hi {first_name} {last_name}, you have successfully registered. Please sign in now.")
                return redirect('login')

            except Exception as e:
                # print(e, 'exception -----------=========================================!!!!!!!!!!!!!!!!!!!')
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
            # print('testing-------------------------')
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
    """"""
    """ If users forgot password """
    if request.method == "POST":
        user_email = request.POST.get('email', '')
        # print(user_email)
        try:
            user = User.objects.get(email=user_email)
            if user.email == user_email:
                security_code = send_forgot_pass_email(user_email)  # sending email to the users email
                print(security_code, 'after send email the code,,,,,,,')
            else:
                messages.error(request, 'Email is not matched with any user')
                return render(request, 'accounts/forgotPass01.html')

            # setting the security_code and user email in the session
            # so that can check with the user given code
            request.session['SECURITY_CODE'] = security_code
            request.session['EMPLOYEE_EMAIL'] = user_email
            messages.success(request, 'A 6 digit  code is send to your email')
            return render(request, 'accounts/forgotPass02.html')
        except Exception as e:
            print(e)
            # messages.error(request, 'error:', e)
            return render(request, 'accounts/forgotPass01.html')

    else:
        return render(request, 'accounts/forgotPass01.html')


def send_forgot_pass_email(email):
    """"""
    """SEnding the email with a random code to the user"""
    code = ""
    for _ in range(6):
        code += str(random.randint(1, 9))
    # print(code)
    # print(credentials.email, email)

    send_mail(
        'Online Project Tracking System - Forgot Password',  # subject
        'Here is the 6 digit Security Code: ' + code + '. Do not share the code. Do not replay.',  # message
        credentials.email,  # from
        [email],  # to
        fail_silently=False,
    )
    # print('send the mail....')

    # email = EmailMessage(
    #     'Hello',
    #     'Body goes here',
    #     credentials.email,
    #     ['yourmail@gmail.com'])
    # email.send()
    # print(email)

    return code


def security_code_view(request):
    """ If users forgot password """
    if request.method == "POST":
        security_code = request.POST['securityCode']  # Collecting security code
        SECURITY_CODE = request.session['SECURITY_CODE']
        if SECURITY_CODE == security_code:
            print(SECURITY_CODE)
            return render(request, 'accounts/changePassword.html')
        else:
            del request.session['SECURITY_CODE']  # False attemp DELETE session
            del request.session['EMPLOYEE_ID']  # False attemp DELETE session
            messages.error(request, 'Invalid Security Code')
            return render(request, 'accounts/forgotPass01.html')
    else:
        return render(request, 'accounts/forgotPass02.html')


def change_password_view(request):
    render(request, 'accounts/changePassword.html')


@login_required(login_url='login')
@has_access_dashboard(
    allowed_roles=[role_super_user, role_pm, role_team_leader, role_team_member, role_tester, role_employee,
                   role_department_head])
def user_profile(request):
    user = get_object_or_404(User, id=request.user.id)
    recent_work = []

    if request.user.role.name == role_pm:
        recent_work = Project.objects.all()[:3]
    elif request.user.role.name == role_department_head:
        recent_work = Project.objects.filter(department=request.user.department).order_by('assigned_at')[:3]
    elif request.user.role.name == role_team_leader:
        recent_work = Module.objects.filter(assigned_team=request.user.team_member).order_by('assigned_at')[:3]
    elif request.user.role.name == role_team_member:
        recent_work = Task.objects.filter(assigned_member=request.user.id).order_by('assigned_at')[:3]
    # elif request.user.role.name == role_tester:
    #     recent_work = SubmittedToQATask.objects.filter(assigned_member=request.uesr.id).order_bY('assigned_at')[:3]

    update_error_render_location = 'accounts/user_profile.html'
    context = {'user': user, 'recent_work': recent_work}

    if request.method == 'POST' and 'basic_information' in request.POST:
        first_name = request.POST.get('first_name')
        middle_name = request.POST.get('middle_name')
        last_name = request.POST.get('last_name')
        gender = request.POST.get('gender')
        birth_date = request.POST.get('birth_date')
        address = request.POST.get('address')
        profile_picture = request.FILES.get('profile_picture')

        date_obj = datetime.strptime(birth_date, '%Y-%m-%d')  # converting string date to date obj
        birth_date_obj = date_obj.date()

        try:
            user.first_name = first_name
            user.middle_name = middle_name
            user.last_name = last_name
            user.gender = gender
            user.address = address
            user.birth_date = birth_date_obj

            # FileSystemStorage for save the file (image)
            file_system_obj = FileSystemStorage()
            if profile_picture is not None:
                # if profile picture is not uploaded then profile_picture = None
                profile_picture_name = file_system_obj.save(profile_picture.name,
                                                            profile_picture)  # saving file
                # ----- checking the file is image or not -----------
                if str(profile_picture.content_type).startswith('image'):

                    # profile_picture.content_type returns "image/png". so to check it is image we use startwith('image')
                    if profile_picture.size < 1000000:
                        # checking the size is less than 1 mb
                        user.profile_picture = profile_picture_name
                        # print('------------- saving data with image')
                        user.save()

                        # print(f"{user.username}'s information is successfully updated.")
                        messages.success(request, f"Profile is updated.")
                        return redirect('user-profile')
                    else:
                        # print('image is grater than 1 mb', profile_picture.size)
                        messages.error(request, 'Image size is greater than 1 mb')
                        file_system_obj.delete(profile_picture_name)
                        return render(request, update_error_render_location, context)
                else:
                    # print('this is not image', profile_picture.content_type)
                    messages.error(request, 'Please upload an image')
                    file_system_obj.delete(profile_picture_name)
                    return render(request, update_error_render_location, context)
            else:
                # print('------------- saving data without image')
                user.save()

                # print(f"{user.username}'s information is successfully updated.")
                messages.success(request, f"{user.username}'s information is updated.")
                return redirect('user-profile')
        except Exception as e:
            # print(e, 'exception ---at user profile update !!!!!!')
            messages.error(request, f"Error: {e}")
            return render(request, update_error_render_location, context)

    elif request.method == 'POST' and 'account-data' in request.POST:
        username = str(request.POST.get('username')).strip()
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        new_password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        try:

            # Validating the information
            if User.objects.filter(username=username).exclude(username=user.username).exists():
                messages.warning(request, f"Username '{username}' is already exists!")
                return render(request, update_error_render_location, context)

            elif User.objects.filter(email=email).exclude(email=user.email).exists():
                messages.warning(request, f"Email '{email}' is already exists!")
                return render(request, update_error_render_location, context)

            else:
                try:
                    user.username = username
                    user.email = email
                    user.mobile_number = phone
                    if new_password and confirm_password:
                        if new_password != confirm_password:
                            messages.error(request, 'Your password is not matched!')
                            return render(request, update_error_render_location, context)
                        else:
                            user.set_password(new_password)
                        user.save()
                    user.save()
                    messages.success(request, f"{user.username}'s account information is updated.")
                    return redirect('user-profile')

                except Exception as e:
                    # print(e, 'exception ---at user profiles account data update !!!!!!')
                    messages.error(request, f"Error: {e}")
                    return render(request, update_error_render_location, context)

        except Exception as e:
            # print(e, 'exception ---at user profiles account data update !!!!!!')
            messages.error(request, f"Error: {e}")
            return render(request, update_error_render_location, context)

    elif request.method == 'POST' and 'social-info' in request.POST:
        facebook_url = request.POST.get('facebook')
        github_url = request.POST.get('github')
        linkedin_url = request.POST.get('linkedin')
        twitter_url = request.POST.get('twitter')

        try:
            user.github_url = github_url
            user.facebook_url = facebook_url
            user.twitter_url = twitter_url
            user.linkedin_url = linkedin_url
            user.save()
            messages.success(request, f"{user.username}'s social information is updated.")
            return redirect('user-profile')

        except Exception as e:
            # print(e, 'exception ---at user profile update !!!!!!')
            messages.error(request, f"Error: {e}")
            return render(request, update_error_render_location, context)
        #     return redirect('employee-list')

    return render(request, 'accounts/user_profile.html', context)
