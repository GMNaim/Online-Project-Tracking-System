# // projectmanager/views.py
import json
import random
import re
from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.core.files.storage import FileSystemStorage
from django.forms import model_to_dict
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect

from accounts.decorators import has_access
from accounts.models import Role, User
from departments.models import Department
from projectmanager.models import Client, Project, TaskHistory
# Role Names
from teams.models import Team

# from teams.models import Membership

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

# for unique random number
random.seed(datetime.now())


def sidebar_department_name(request):
    sidebar_department_name = ''
    if request.user.department.id != 16:
        sidebar_department_name = request.user.department.name
        return sidebar_department_name


@login_required(login_url='login')
@has_access(allowed_roles=[role_pm, role_super_user])
def employee_add(request):
    sidebar_department_name(request)

    print(str(request.user.groups.all()[0]))
    role_list = Role.objects.exclude(name__iexact=role_super_user)
    department_list = Department.objects.all()
    existence_department_head = [user.department.name for user in
                                 User.objects.filter(role__name__iexact=role_department_head)]
    # free_department_head = [(user.department.name) for user in User.objects.filter(
    #     role__name__in=['Admin', 'Super User', 'Team Leader', 'Team Member', 'Employee'])]
    not_assigned_dep_head = []
    for dep in department_list:
        if dep.name not in existence_department_head:
            not_assigned_dep_head.append(dep)
    # print(not_assigned_dep_head, '*********************************')
    # for n in not_assigned_dep_head:
    #     print(n.name, n.id)
    # free_department_head = User.objects.filter(
    #     role__name__in=['Admin', 'Super User', 'Team Leader', 'Team Member', 'Employee']).values_list('department__name', flat=True)
    # print(free_department_head, '---------------------------------------------------------- free department')
    all_department = [{'id': department.id, 'name': department.name} for department in department_list]
    # print(all_department, '=======================df=df=df')
    # print('existence department', existence_department_head)
    context = {'role_list': role_list, 'department_list': department_list, 'default_password': default_password,
               'existence_department_head': existence_department_head, 'free_department_head': not_assigned_dep_head,
               'all_department': json.dumps(all_department),
               'sidebar_department_name': sidebar_department_name(request)}  # creating string by dumps
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        middle_name = request.POST.get('middle_name', '')
        last_name = request.POST.get('last_name', '')
        username = str(request.POST.get('username')).strip()
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        address = request.POST.get('address', '')
        gender = request.POST.get('gender')
        profile_picture = request.FILES.get('profile_picture')
        role = Role.objects.get(id=int(request.POST.get('role')))
        department = request.POST.get('department')
        if department == '':
            department = request.POST.get('department_h')
        if department == '':
            department = Department.objects.get(id=16)
        else:
            department = Department.objects.get(id=int(department))

        # print(type(first_name), middle_name, last_name, username, email, phone, password, address, gender,
        #       profile_picture, role, type(role), department)

        context = {'first_name': first_name, 'middle_name': middle_name, 'last_name': last_name, "username": username,
                   'email': email, 'phone': phone, 'password': password, 'address': address, 'gender': gender,
                   'role': role, 'role_list': role_list, 'department_list': department_list,
                   'default_password': default_password,
                   'existence_department_head': existence_department_head,
                   'free_department_head': not_assigned_dep_head, 'all_department': json.dumps(all_department),
                   'sidebar_department_name': sidebar_department_name}

        # Validating the information
        employee_add_error_link = 'projectmanager/employee_add.html'
        if username.strip() == "":
            messages.warning(request, 'You must have to provide an username')
            return render(request, employee_add_error_link, context)

        elif User.objects.filter(username=username).exists():
            messages.warning(request, f"Username {username} is already exists!")
            return render(request, employee_add_error_link, context)

        elif re.match(r"^[a-zA-Z0-9_.-]+$", username) is None:
            messages.warning(request, f"Username {username} is not valid! Please provide a valid username")
            return render(request, employee_add_error_link, context)

        elif email.strip() == "":
            messages.warning(request, 'You must have to provide a email!')
            return render(request, employee_add_error_link, context)

        elif User.objects.filter(email=email).exists():
            messages.warning(request, f"Email {email} is already exists!")
            return render(request, employee_add_error_link, context)

        elif first_name.strip() == "":
            messages.warning(request, f"Please Provide first name!")
            return render(request, employee_add_error_link, context)

        elif phone.strip() == "":
            messages.warning(request, f"Please Provide your phone number!")
            return render(request, employee_add_error_link, context)

        elif gender == "":
            messages.warning(request, f"Please Provide your gender!")
            return render(request, employee_add_error_link, context)

        elif str(role.name) == "":
            messages.warning(request, f"Please Select a role!")
            return render(request, employee_add_error_link, context)

        elif role == role_department_head and department.name in existence_department_head:
            messages.warning(request, f"{department.name} has a department head.")
            return render(request, employee_add_error_link, context)

        else:
            """Adding user in the database"""
            try:
                user = User()
                user.first_name = first_name
                user.middle_name = middle_name
                user.last_name = last_name
                user.username = username
                user.email = email
                user.mobile_number = phone
                user.address = address
                user.gender = gender
                user.role = role
                user.department = department
                if password == "":
                    user.set_password(default_password)
                else:
                    user.set_password(password)
                if str(role) == role_tester:
                    user.is_tester = True

                file_system_obj = FileSystemStorage()
                if profile_picture is not None:
                    # if profile picture is not uploaded then profile_picture = None
                    profile_picture_name = file_system_obj.save(profile_picture.name,
                                                                profile_picture)  # saving file
                    # ----- checking the file is image or not -----------
                    if str(profile_picture.content_type).startswith('image'):

                        # profile_picture.content_type returns "image/png". so to check it is image
                        # we use startswith('image')
                        if profile_picture.size < 1000000:
                            # checking the size is less than 1 mb
                            user.profile_picture = profile_picture_name
                            # print('------------- saving data')
                            user.save()

                            """============ Adding group to the new users ============"""
                            group_employee.user_set.add(user)  # all user is an employee
                            if str(role) == role_pm:
                                group_pm.user_set.add(user)
                            elif str(role) == role_super_user:
                                group_super_user.user_set.add(user)
                            elif str(role) == role_department_head:
                                group_department_head.user_set.add(user)
                            elif str(role) == role_team_leader:
                                group_team_leader.user_set.add(user)
                            elif str(role) == role_team_member:
                                group_team_member.user_set.add(user)
                            elif str(role) == role_employee:
                                group_employee.user_set.add(user)
                            elif str(role) == role_tester:
                                group_tester.user_set.add(user)

                            # print(f"{username}' is successfully added to the database.")
                            messages.success(request, f"{username} is added to the database.")
                            return redirect('employee-list')
                        else:
                            # print('image is grater than 1 mb', profile_picture.size)
                            messages.error(request, 'Image size is greater than 1 mb')
                            file_system_obj.delete(profile_picture_name)
                            return render(request, 'projectmanager/employee_add.html', context)
                    else:
                        # print('this is not image', profile_picture.content_type)
                        messages.error(request, 'Please upload an image')
                        file_system_obj.delete(profile_picture_name)
                        return render(request, 'projectmanager/employee_add.html', context)
                else:
                    # print('------------- saving data without image')
                    user.save()

                    """ Adding group to the new users"""
                    group_employee.user_set.add(user)  # all user is an employee
                    if str(role) == role_pm:
                        group_pm.user_set.add(user)
                    elif str(role) == role_super_user:
                        group_super_user.user_set.add(user)
                    elif str(role) == role_department_head:
                        group_department_head.user_set.add(user)
                    elif str(role) == role_team_leader:
                        group_team_leader.user_set.add(user)
                    elif str(role) == role_team_member:
                        group_team_member.user_set.add(user)
                    elif str(role) == role_employee:
                        group_employee.user_set.add(user)
                    elif str(role) == role_tester:
                        group_tester.user_set.add(user)

                    # print(f"{username}'s information is successfully saved.")
                    messages.success(request, f"{username} is added.")
                    return redirect('employee-list')
            except Exception as e:
                print(e, 'exception -----at empoyee add !!!')
                messages.error(request, f"Error: {e}")
                return render(request, 'projectmanager/employee_add.html')
            #     return redirect('employee-list')

    return render(request, 'projectmanager/employee_add.html', context)


@login_required(login_url='login')
@has_access(allowed_roles=[role_pm, role_super_user])
def employee_update(request, employee_username):
    if request.user.is_authenticated:
        # print('employee is authenticated ---------')
        employee = get_object_or_404(User, username=employee_username)
        role_list = Role.objects.exclude(name__iexact=role_super_user)
        department_list = Department.objects.all()
        existence_department_head = [user.department.name for user in
                                     User.objects.filter(role__name__iexact=role_department_head)]

        not_assigned_dep_head = []
        for dep in department_list:
            if dep.name not in existence_department_head:
                not_assigned_dep_head.append(dep)
        # print(not_assigned_dep_head, '*********************************')
        # for n in not_assigned_dep_head:
        #     print(n.name, n.id)

        context = {'role_list': role_list, 'department_list': department_list, 'employee': employee,
                   'default_password': default_password,
                   'free_department_head': not_assigned_dep_head,
                   'existence_department_head': existence_department_head}
        if request.method == "POST":
            first_name = request.POST.get('first_name')
            middle_name = request.POST.get('middle_name')
            last_name = request.POST.get('last_name')
            username = str(request.POST.get('username')).strip()
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            password = request.POST.get('password')
            address = request.POST.get('address')
            gender = request.POST.get('gender')
            profile_picture = request.FILES.get('profile_picture')
            role = Role.objects.get(id=int(request.POST.get('role')))
            department = request.POST.get('department')
            if department == '':
                department = request.POST.get('department_h')
            if department == '':
                department = Department.objects.get(id=16)
            else:
                department = Department.objects.get(id=int(department))

            # print(type(first_name), middle_name, last_name, username, email, phone, password, address, gender,
            #       profile_picture, department, role)
            # print('existence_department_head', existence_department_head)

            context = {'first_name': employee.first_name, 'middle_name': employee.middle_name,
                       'last_name': employee.last_name, "username": employee.username,
                       'email': employee.email, 'phone': employee.mobile_number, 'password': employee.password,
                       'address': employee.address, 'gender': employee.gender,
                       'role': employee.role, 'role_list': role_list, 'department_list': department_list,
                       'department': department, 'default_password': default_password,
                       'employee': employee, 'existence_department_head': existence_department_head}

            update_error_render_location = 'projectmanager/employee_update.html'

            # Validating the information
            if username.strip() == "":
                messages.warning(request, 'You must have to provide an username')
                return render(request, update_error_render_location, context)

            elif User.objects.filter(username=username).exclude(username=employee.username).exists():

                messages.warning(request, f"Username '{username}' is already exists!")
                return render(request, update_error_render_location, context)

            elif email.strip() == "":
                messages.warning(request, 'You must have to provide a email!')
                return render(request, update_error_render_location, context)

            elif User.objects.filter(email=email).exclude(email=employee.email).exists():
                messages.warning(request, f"Email '{email}' is already exists!")
                return render(request, update_error_render_location, context)

            elif first_name.strip() == "":
                messages.warning(request, f"Please Provide first name!")
                return render(request, update_error_render_location, context)

            elif phone.strip() == "":
                messages.warning(request, f"Please Provide your phone number!")
                return render(request, update_error_render_location, context)

            elif gender == "":
                messages.warning(request, f"Please Provide your gender!")
                return render(request, update_error_render_location, context)

            elif str(role) == "":
                messages.warning(request, f"Please Select a role!")
                return render(request, update_error_render_location, context)

            elif (
                    role == role_department_head and department.name in existence_department_head) and employee.department.name != department.name:
                messages.warning(request, f"{department.name} has a department head.")
                return render(request, update_error_render_location, context)
            else:
                # ========= UPDATING THE EMPLOYEE ==============
                try:
                    employee.username = username
                    employee.email = email
                    employee.first_name = first_name
                    employee.middle_name = middle_name
                    employee.last_name = last_name
                    employee.gender = gender
                    employee.mobile_number = phone
                    employee.address = address

                    if employee.department != department:  # if employee's dep is changed then he will be a employee
                        # and remove older status....
                        employee.role = Role.objects.get(name__iexact=role_employee)
                        employee.is_team_leader = False
                        employee.is_tester = False
                        employee.team_member = Team.objects.get(id=10)
                        employee.groups.clear()  # clearing all groups form the employee
                        group_employee.user_set.add(employee)
                    else:
                        employee.role = role

                    employee.department = department
                    if password == "":
                        employee.set_password(default_password)
                    else:
                        employee.set_password(password)
                    if str(role) == role_tester:
                        employee.is_tester = True
                    elif str(role) != role_tester:
                        employee.is_tester = False
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
                                employee.profile_picture = profile_picture_name
                                # print('------------- saving data with image')
                                employee.save()

                                """ Adding group to the new users"""
                                employee.groups.clear()  # clearing all groups form the employee
                                group_employee.user_set.add(employee)
                                if str(employee.role.name) == role_pm:
                                    group_pm.user_set.add(employee)
                                elif str(employee.role.name) == role_super_user:
                                    group_super_user.user_set.add(employee)
                                elif str(employee.role.name) == role_department_head:
                                    group_department_head.user_set.add(employee)
                                elif str(employee.role.name) == role_team_leader:
                                    group_team_member.user_set.add(employee)
                                    group_team_leader.user_set.add(employee)
                                elif str(employee.role.name) == role_team_member:
                                    group_team_member.user_set.add(employee)
                                elif str(employee.role.name) == role_employee:
                                    group_employee.user_set.add(employee)
                                elif str(employee.role.name) == role_tester:
                                    group_tester.user_set.add(employee)

                                # print(f"{employee.username}'s information is successfully updated.")
                                messages.success(request, f"{employee.username}'s information is updated.")
                                return redirect('employee-list')
                            else:
                                # print('image is grater than 1 mb', profile_picture.size)
                                messages.error(request, 'Image size is greater than 1 mb')
                                file_system_obj.delete(profile_picture_name)
                                return render(request, 'projectmanager/employee_update.html', context)
                        else:
                            # print('this is not image', profile_picture.content_type)
                            messages.error(request, 'Please upload an image')
                            file_system_obj.delete(profile_picture_name)
                            return render(request, 'projectmanager/employee_update.html', context)
                    else:
                        # print('------------- saving data without image')
                        employee.save()
                        """ Adding group to the new users"""
                        employee.groups.clear()  # clearing all groups form the employee
                        group_employee.user_set.add(employee)
                        if str(employee.role.name) == role_pm:
                            group_pm.user_set.add(employee)
                        elif str(employee.role.name) == role_super_user:
                            group_super_user.user_set.add(employee)
                        elif str(employee.role.name) == role_department_head:
                            group_department_head.user_set.add(employee)
                        elif str(employee.role.name) == role_team_leader:
                            group_team_member.user_set.add(employee)
                            group_team_leader.user_set.add(employee)
                        elif str(employee.role.name) == role_team_member:
                            group_team_member.user_set.add(employee)
                        elif str(employee.role.name) == role_employee:
                            group_employee.user_set.add(employee)
                        elif str(employee.role.name) == role_tester:
                            group_tester.user_set.add(employee)

                        # print(f"{employee.username}'s information is successfully updated.")
                        messages.success(request, f"{employee.username}'s information is updated.")
                        return redirect('employee-list')
                except Exception as e:
                    print(e, 'exception ---at empoyee update !!!!!!')
                    messages.error(request, f"Error: {e}")
                    return render(request, 'projectmanager/employee_update.html')
                #     return redirect('employee-list')

        return render(request, 'projectmanager/employee_update.html', context)


@login_required(login_url='login')
@has_access(allowed_roles=[role_pm, role_super_user])
def employee_delete(request, employee_username):
    if request.user.is_authenticated:
        user = User.objects.exclude(role__name__iexact=role_super_user)
        context = {'employee_list': user}
        employee = get_object_or_404(User, username=employee_username)
        try:
            employee.delete()
            messages.success(request, f"Employee '{employee.username}' is deleted!")
            return redirect('employee-list')
        except employee.DoesNotExist:
            messages.error(request, 'Employee does not exist')
            return redirect('employee-list')
        except Exception as e:
            messages.error(request, f"Error: {e}.")

        return render(request, 'projectmanager/employee_list.html', context)


@login_required(login_url='login')
@has_access(allowed_roles=[role_pm, role_super_user])
def employee_list(request):
    user = User.objects.exclude(role__name__iexact=role_super_user)
    context = {'employee_list': user, 'selected': True}

    return render(request, 'projectmanager/employee_list.html', context)


"""=======================================     CLIENT WORK    ==========================================="""


@login_required(login_url='login')
@has_access(allowed_roles=[role_pm, role_super_user])
def client_list(request):
    if request.user.is_authenticated:
        client = Client.objects.all()
        context = {'client_list': client}
        return render(request, 'projectmanager/client_list.html', context)


@login_required(login_url='login')
@has_access(allowed_roles=[role_pm, role_super_user])
def client_add(request):
    if request.user.is_authenticated:
        all_client = Client.objects.all()

        if request.method == "POST":
            name = str(request.POST['name']).strip()
            email = request.POST['email']
            phone = request.POST['phone']
            company_name = request.POST['company_name']
            address = request.POST['address']
            comment = request.POST['comment']
            profile_picture = request.FILES.get('profile_picture')
            # print(name, phone, company_name, address, email, comment,
            #       profile_picture)

            context = {'name': name, 'email': email, 'phone': phone,
                       'company_name': company_name,
                       'address': address, 'comment': comment}
            # Validating the information
            client_add_error_link = 'projectmanager/client_add.html'
            if name.strip() == "":
                messages.warning(request, 'Please provide client name')
                return render(request, client_add_error_link, context)

            elif email.strip() == "":
                messages.warning(request, 'You must have to provide a email!')
                return render(request, client_add_error_link, context)

            elif Client.objects.filter(email=email).exists():
                messages.warning(request, f"Email {email} is already exists for another client!")
                return render(request, client_add_error_link, context)

            elif phone.strip() == "":
                messages.warning(request, f"Please Provide client phone number!")
                return render(request, client_add_error_link, context)

            else:
                try:
                    #  Creating random client id
                    ran_num = random.randint(1000, 99999)
                    client_random_id = "client" + str(ran_num)
                    for client in all_client:
                        if client.client_id == client_random_id:
                            ran_num = random.randint(1000, 99999)
                            client_random_id = "client" + str(ran_num)
                    #  Adding client to the database
                    client = Client(name=name, client_id=client_random_id, email=email, phone=phone,
                                    company_name=company_name, comment=comment, address=address)

                    file_system_obj = FileSystemStorage()
                    if profile_picture is not None:
                        # if profile picture is not uploaded then profile_picture = None
                        profile_picture_name = file_system_obj.save(profile_picture.name,
                                                                    profile_picture)  # saving file
                        # ----- checking the file is image or not -----------
                        if str(profile_picture.content_type).startswith('image'):
                            # profile_picture.content_type returns "image/png". so to check it is image
                            # we use startswith('image')
                            if profile_picture.size < 1000000:
                                # checking the size is less than 1 mb
                                client.profile_picture = profile_picture_name
                                # print('------------- saving data')
                                client.save()
                                # print(f"{client}' is successfully added to the database.")
                                messages.success(request, f"{client} is added to the database.")
                                return redirect('client-list')
                            else:
                                # print('image is grater than 1 mb', profile_picture.size)
                                messages.error(request, 'Image size is greater than 1 mb')
                                file_system_obj.delete(profile_picture_name)
                                return render(request, 'projectmanager/client_add.html')
                        else:
                            # print('this is not image', profile_picture.content_type)
                            messages.error(request, 'Please upload an image')
                            file_system_obj.delete(profile_picture_name)
                            return render(request, 'projectmanager/client_add.html')
                    else:
                        # print('------------- saving data without image')
                        client.save()
                        # print(f"Client {name}'s information is successfully saved.")
                        messages.success(request, f"Client '{name}' is added to the database.")
                        return redirect('client-list')

                except Exception as e:
                    print(e, 'exception --at client add!!')
                    messages.error(request, f"Error: {e}")
                    return render(request, 'projectmanager/client_add.html')

        return render(request, 'projectmanager/client_add.html')


@login_required(login_url='login')
@has_access(allowed_roles=[role_pm, role_super_user])
def client_update(request, client_id):
    if request.user.is_authenticated:
        selected_client = get_object_or_404(Client, client_id=client_id)
        context = {'name': selected_client.name, 'client_id': selected_client.client_id,
                   'email': selected_client.email, 'phone': selected_client.phone,
                   'company_name': selected_client.company_name,
                   'address': selected_client.address, 'comment': selected_client.comment,
                   'profile_picture': selected_client.profile_picture}

        if request.method == "POST":
            name = str(request.POST['name']).strip()
            email = request.POST['email']
            phone = request.POST['phone']
            company_name = request.POST['company_name']
            address = request.POST['address']
            comment = request.POST['comment']
            profile_picture = request.FILES.get('profile_picture')
            # print(name, client_id, phone, company_name, address, email, comment,
            #       profile_picture)

            # Validating the information
            client_update_error_link = 'projectmanager/client_update.html'
            if name.strip() == "":
                messages.warning(request, 'Please provide client name')
                return render(request, client_update_error_link, context)

            elif email.strip() == "":
                messages.warning(request, 'You must have to provide a email!')
                return render(request, client_update_error_link, context)

            elif Client.objects.filter(email=email).exclude(email=selected_client.email).exists():
                messages.warning(request, f"Email {email} is already exists for another client!")
                return render(request, client_update_error_link, context)

            elif phone.strip() == "":
                messages.warning(request, f"Please Provide client phone number!")
                return render(request, client_update_error_link, context)

            else:
                try:
                    #  Updating the client
                    selected_client.name = name
                    selected_client.email = email
                    selected_client.phone = phone
                    selected_client.company_name = company_name
                    selected_client.comment = comment
                    selected_client.address = address

                    file_system_obj = FileSystemStorage()
                    if profile_picture is not None:
                        # if profile picture is not uploaded then profile_picture = None
                        profile_picture_name = file_system_obj.save(profile_picture.name,
                                                                    profile_picture)  # saving file
                        # ----- checking the file is image or not -----------
                        if str(profile_picture.content_type).startswith('image'):
                            # profile_picture.content_type returns "image/png". so to check it is image
                            # we use startswith('image')
                            if profile_picture.size < 1000000:
                                # checking the size is less than 1 mb
                                selected_client.profile_picture = profile_picture_name
                                # print('------------- saving data')
                                selected_client.save()
                                # print(f"{selected_client.name}' is successfully added to the database.")
                                messages.success(request,
                                                 f"Client {selected_client.name}'s information is successfully updated.")
                                return redirect('client-list')
                            else:
                                # print('image is grater than 1 mb', profile_picture.size)
                                messages.error(request, 'Image size is greater than 1 mb')
                                file_system_obj.delete(profile_picture_name)
                                return render(request, client_update_error_link, context)
                        else:
                            # print('this is not image', profile_picture.content_type)
                            messages.error(request, 'Please upload an image')
                            file_system_obj.delete(profile_picture_name)
                            return render(request, client_update_error_link, context)
                    else:
                        # print('------------- saving data without image')
                        selected_client.save()
                        # print(f"Client {selected_client.name}'s information is successfully updated.")
                        messages.success(request, f"Client '{name}' is added to the database.")
                        return redirect('client-list')

                except Exception as e:
                    print(e, 'exception --at client update!!')
                    messages.error(request, f"Error: {e}")
                    return render(request, client_update_error_link, context)

        return render(request, 'projectmanager/client_update.html', context)


@login_required(login_url='login')
@has_access(allowed_roles=[role_super_user, role_pm])
def client_delete(request, client_id):
    if request.user.is_authenticated:
        selected_client = get_object_or_404(Client, client_id=client_id)

        try:
            selected_client.delete()
            messages.success(request, f"Employee '{selected_client.name}' is deleted!")
            return redirect('client-list')
        except selected_client.DoesNotExist:
            messages.error(request, 'Client does not exist')
            return redirect('client-list')
        except Exception as e:
            messages.error(request, f"Error: {e}.")
            return redirect('client-list')


"""=======================================     PROJECT WORK    ==========================================="""


@login_required(login_url='login')
@has_access(allowed_roles=[role_pm, role_super_user])
def project_add(request):
    if request.user.is_authenticated:
        project_list = Project.objects.all()
        client = Client.objects.all()
        department = Department.objects.exclude(id=16)
        context = {'client_list': client, 'department_list': department}

        if request.method == "POST":
            name = str(request.POST['name']).strip()
            selected_client = request.POST['select_client']
            selected_department = request.POST['select_department']
            description = request.POST['description']
            delivery_date = request.POST['delivery_date']
            # print(name, selected_client, selected_department, description, delivery_date)

            date_obj = datetime.strptime(delivery_date, '%Y-%m-%d')  # converting string date to date obj
            delivery_date_obj = date_obj.date()
            # print('Date:', delivery_date_obj)
            today = datetime.today().date()
            # print(today)
            check_old_date = delivery_date_obj - today  # checking whether given date is old than today
            # print(check_old_date)
            context = {'client_list': client, 'department_list': department, 'name': name, 'description': description,
                       'selected_client': int(selected_client), 'selected_department': int(selected_department),
                       'delivery_date': delivery_date_obj.strftime("%Y-%m-%d")}
            # Validating the information
            project_add_error_link = 'projectmanager/project_add.html'
            if check_old_date.days < 0:
                messages.warning(request, 'Please select a valid delivery date.')
                return render(request, project_add_error_link, context)

            elif name.strip() == "":
                messages.warning(request, 'Please provide a project name')
                return render(request, project_add_error_link, context)

            elif description.strip() == "":
                messages.warning(request, 'Please provide details description.')
                return render(request, project_add_error_link, context)

            elif selected_client == '':
                messages.warning(request, f"Please select a client!")
                return render(request, project_add_error_link, context)

            elif selected_department == '':
                messages.warning(request, f"Please select a department!")
                return render(request, project_add_error_link, context)

            elif delivery_date == '':
                messages.warning(request, f"Please provide delivery date!")
                return render(request, project_add_error_link, context)

            else:
                try:
                    #  Saving data to database
                    #  Creating random project code
                    ran_num = random.randint(1000, 99999)
                    project_random_code = "project-" + name.replace(' ', '-') + str(ran_num)
                    for project in project_list:
                        if project.code == project_random_code:
                            ran_num = random.randint(1000, 99999)
                            project_random_code = "project-" + name.replace(' ', '-') + str(ran_num)

                    selected_client_obj = client.get(id=int(selected_client))
                    selected_department_obj = department.get(id=int(selected_department))
                    # print(selected_client_obj, selected_department_obj)
                    project = Project(name=name,
                                      code=project_random_code,
                                      description=description,
                                      client=selected_client_obj,
                                      department=selected_department_obj,
                                      delivery_date=delivery_date_obj)
                    project.save()
                    messages.success(request, f"Project '{name}' is created successfully!")
                    return redirect('project-list')
                except Exception as e:
                    print("Error at project add===:", e)
                    messages.error(request, e)
                    return render(request, project_add_error_link, context)

        return render(request, 'projectmanager/project_add.html', context)


@login_required(login_url='login')
@has_access(allowed_roles=[role_pm, role_super_user])
def project_update(request, project_code):
    if request.user.is_authenticated:
        selected_project = get_object_or_404(Project, code=project_code)
        client = Client.objects.all()
        department = Department.objects.all()
        context = {'client_list': client, 'department_list': department, 'name': selected_project.name,
                   'description': selected_project.description,
                   'selected_client': selected_project.client, 'selected_department': selected_project.department,
                   'delivery_date': selected_project.delivery_date.strftime("%Y-%m-%d"),
                   'project_code': selected_project.code, 'project_status': selected_project.status}
        # print(type(selected_project.delivery_date), '-------------------------------------')
        # print(selected_project.delivery_date.strftime("%Y-%m-%d"), '-------------------------------------')
        if request.method == "POST":
            name = str(request.POST.get('name', '')).strip()
            selected_client = request.POST.get('select_client', '')
            selected_department = request.POST.get('select_department', '')
            description = request.POST.get('description', '')
            delivery_date = request.POST.get('delivery_date', '')
            project_status = request.POST.get('project_status', '')
            # print(name, selected_client, selected_department, description, delivery_date, project_status, '===')

            date_obj = datetime.strptime(delivery_date, '%Y-%m-%d')  # converting string date to date obj
            delivery_date_obj = date_obj.date()
            # print('Date:', delivery_date_obj)
            today = datetime.today().date()
            # print(today)
            check_old_date = delivery_date_obj - today  # checking whether given date is old than today
            # print(check_old_date)

            # Validating the information
            project_update_error_link = 'projectmanager/project_update.html'
            if check_old_date.days < 0:
                messages.warning(request, 'Please select a valid delivery date.')
                return render(request, project_update_error_link, context)

            elif name.strip() == "":
                messages.warning(request, 'Please provide a project name')
                return render(request, project_update_error_link, context)

            elif description.strip() == "":
                messages.warning(request, 'Please provide details description.')
                return render(request, project_update_error_link, context)

            elif selected_client == '':
                messages.warning(request, f"Please select a client!")
                return render(request, project_update_error_link, context)

            elif selected_department == '':
                messages.warning(request, f"Please select a department!")
                return render(request, project_update_error_link, context)

            elif delivery_date == '':
                messages.warning(request, f"Please provide delivery date!")
                return render(request, project_update_error_link, context)

            else:
                try:
                    #  Updating data to database
                    selected_client_obj = client.get(id=int(selected_client))
                    selected_department_obj = department.get(id=int(selected_department))
                    # print(selected_client_obj, selected_department_obj)

                    selected_project.name = name
                    selected_project.description = description
                    selected_project.client = selected_client_obj
                    # selected_project.department = selected_department_obj   # setting below...
                    selected_project.delivery_date = delivery_date_obj
                    # if project_status != '':
                    #     selected_project.status = int(project_status)
                    # selected_project.save()

                    """ Setting notification as project is assigned or removed to or from a head """
                    # Getting the assigned dep head
                    previously_assigned_head = User.objects.get(department=selected_project.department,
                                                                role__name__iexact=role_department_head)

                    """ If project is assigned already to a dep and then only change the dep then notification count"""

                    if (project_status == '' or int(
                            project_status) == 1) and selected_department_obj != selected_project.department and selected_project.status == 2:
                        print('1')
                        previously_assigned_head.notification_count += 1  # increase previous head notification count to tell that project is removed from him
                        previously_assigned_head.save()
                        # create new task history object
                        task_history = TaskHistory()
                        task_history.project = selected_project
                        task_history.description = (model_to_dict(selected_project))
                        task_history.status = 'Project Removed'
                        task_history.user = previously_assigned_head
                        task_history.save()
                        # if previously_assigned_head.notification_count < 0:  # if notification count is < than 0
                        #     previously_assigned_head.notification_count = 0  # then make it 0
                        #     previously_assigned_head.save()

                        if project_status == '' or int(project_status) == 1:
                            selected_project.status = 1  # then change the status of the project to new
                            selected_project.assigned_at = None  # setting NOne as the status is new or not assigned
                            selected_project.save()

                        """If project is assigned already to a dep and then change both the dep and 
                       status to assigned at the same time """
                    elif project_status != '' and selected_department_obj != selected_project.department and int(
                            project_status) == 2:
                        print('2')
                        # print('enter into same time change')
                        # print(selected_project in Project.objects.filter(department=selected_project.department, status=2), '----6565')

                        if selected_project in Project.objects.filter(department=selected_project.department, status=2):
                            previously_assigned_head.notification_count += 1  # increase previous head notification count to tell that project is removed from
                            previously_assigned_head.save()

                            task_history = TaskHistory()
                            task_history.project = selected_project
                            task_history.description = (model_to_dict(selected_project))
                            task_history.status = 'Project Removed'
                            task_history.user = previously_assigned_head
                            task_history.save()

                        # adding the module to the new leader
                        selected_project.department = selected_department_obj
                        selected_project.save()
                        new_dep_head_with_assigned_project_same_time = selected_project.department.employee_department.get(
                            role__name__iexact=role_department_head)
                        new_dep_head_with_assigned_project_same_time.notification_count += 1
                        new_dep_head_with_assigned_project_same_time.save()
                        selected_project.status = 2
                        selected_project.assigned_at = datetime.now()
                        selected_project.save()
                        # create new task history object
                        task_history = TaskHistory()
                        task_history.project = selected_project
                        task_history.description = (model_to_dict(selected_project))
                        task_history.status = 'New Project'
                        task_history.user = new_dep_head_with_assigned_project_same_time
                        task_history.save()

                        """ Assign project  to head in edit mode then notification count..."""
                    elif project_status != '' and selected_project.status != 2 and int(project_status) == 2:
                        print('3')
                        # if selected project previous status not 2 means not assigned and user select 2 then...
                        previously_assigned_head.notification_count += 1  # Then increase the notification count
                        selected_project.assigned_at = datetime.now()  # after assigning the project setting date.
                        selected_project.save()
                        previously_assigned_head.save()
                        # create new task history object
                        task_history = TaskHistory()
                        task_history.project = selected_project
                        task_history.description = (model_to_dict(selected_project))
                        task_history.status = 'New Project'
                        task_history.user = previously_assigned_head
                        task_history.save()

                        """ just change the status of the project from assigned to new"""
                    elif (project_status == '' or int(project_status) == 1) and selected_project.status == 2:
                        print('4')
                        # if module previous status is 2 and user select 1 then only do --
                        previously_assigned_head.notification_count += 1  # increase previous head notification count to tell that project is removed from
                        previously_assigned_head.save()
                        selected_project.assigned_at = None  # setting NOne as the status is set new or not assigned
                        selected_project.save()
                        # create new task history object
                        task_history = TaskHistory()
                        task_history.project = selected_project
                        task_history.description = (model_to_dict(selected_project))
                        task_history.status = 'Project Removed'
                        task_history.user = previously_assigned_head
                        task_history.save()
                        # if previously_assigned_head.notification_count < 0:  # if notification count is < than 0
                        #     previously_assigned_head.notification_count = 0  # then n.c. is 0
                        #     previously_assigned_head.save()
                    # setting status, department here because of notification count.
                    # if set up then got wrong notification count value cause we checked db value of previous status
                    # which is updated by doing following thing.
                    if project_status != '':  # '' means not select any status.
                        print('5')
                        selected_project.status = int(project_status)
                    selected_project.department = selected_department_obj  # if change dep after assigned to a dep thats why setting here not top
                    selected_project.save()
                    messages.success(request, f"Project '{name}' updated successfully!")
                    return redirect('project-list')

                except Exception as e:
                    print("Error at project update===", e)
                    messages.error(request, e)
                    return render(request, project_update_error_link, context)

        return render(request, 'projectmanager/project_update.html', context)


@login_required(login_url='login')
@has_access(allowed_roles=[role_pm, role_super_user])
def project_list(request):
    projects = Project.objects.all().order_by('-created_at')

    """ CHANGING THE NOTIFICATION COUNT TO ZERO as he see the notification"""
    # current_user = User.objects.get(id=request.user.id)
    # current_user.notification_count = 0
    # current_user.save()

    context = {'projects': projects}
    return render(request, 'projectmanager/project_list.html', context)


@login_required(login_url='login')
@has_access(allowed_roles=[role_super_user, role_pm])
def project_delete(request, project_code):
    if request.user.is_authenticated:
        selected_project = get_object_or_404(Project, code=project_code)

        try:
            selected_project.delete()
            messages.success(request, f"Project '{selected_project.name}' is deleted!")
            return redirect('project-list')

        except selected_project.DoesNotExist:
            messages.error(request, 'Project does not exist')
            return redirect('project-list')

        except Exception as e:
            messages.error(request, f"Error: {e}.")
            return redirect('project-list')


@login_required(login_url='login')
@has_access(allowed_roles=[role_pm, role_super_user])
def project_assign(request, project_code):
    """
    After clicking on the assign project this funcation will run
    it will change the status of the project new to assigned
    """
    if request.user.is_authenticated:
        projects = Project.objects.all()
        context = {'projects': projects}
        selected_project = get_object_or_404(Project, code=project_code)
        try:
            selected_project.status = 2  # project is assigned
            selected_project.save()

            # getting the head
            assigned_head = User.objects.get(department=selected_project.department,
                                             role__name__iexact=role_department_head)
            # create new task history object
            task_history = TaskHistory()
            task_history.project = selected_project
            task_history.description = (model_to_dict(selected_project))
            task_history.status = 'New Project'
            task_history.user = assigned_head
            task_history.save()

            """ Setting notification as project is assigned to a head """
            assigned_head.notification_count += 1
            assigned_head.save()
            selected_project.assigned_at = datetime.now()  # setting the assigned time
            selected_project.save()
            # print(assigned_head, '------------------------------------------*********************',
            #       assigned_head.notification_count)
            messages.success(request, f"Project '{selected_project.name}' is assigned to the department head.")
            return redirect('project-list')
        except Exception as e:
            print('error at assign project ====', e)
            messages.error(request, f"Error: {e}")
            return render(request, 'projectmanager/project_list.html', context)
