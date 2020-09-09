from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect

from accounts.models import Role, User
from departments.models import Department

import json

default_password = 'test123'


@login_required
def dashboard(request):
    total_employee = User.objects.filter(is_active=True).count()
    total_department = Department.objects.filter(is_active=True).count()
    context = {'total_employee': total_employee, 'total_department': total_department}
    return render(request, 'adminusers/dashboard.html', context)


@login_required
def client_list(request):
    return render(request, 'adminusers/client_list.html')


@login_required
def client_add(request):
    return render(request, 'adminusers/client_add.html')


@login_required
def project_add(request):
    return render(request, 'adminusers/project_add.html')


@login_required
def project_list(request):
    return render(request, 'adminusers/project_list.html')


@login_required
def employee_list(request):
    user = User.objects.exclude(role__name__iexact='Super Admin')
    context = {'employee_list': user}

    return render(request, 'adminusers/employee_list.html', context)


@login_required
def employee_add(request):
    role_list = Role.objects.exclude(name__iexact='Super Admin')
    department_list = Department.objects.all()
    existence_department_head = [user.department.name for user in User.objects.filter(role__name__iexact='Department Head')]
    all_department = [{'id': department.id, 'name': department.name} for department in department_list]
    print(all_department, '=======================df=df=df')
    print('existence department', existence_department_head)
    context = {'role_list': role_list, 'department_list': department_list, 'default_password': default_password,
               'existence_department_head': existence_department_head, 'all_department': json.dumps(all_department)} # creating string by dumps
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        middle_name = request.POST.get('middle_name', '')
        last_name = request.POST.get('last_name', '')
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        address = request.POST.get('address', '')
        gender = request.POST.get('gender')
        profile_picture = request.FILES.get('profile_picture')
        role = Role.objects.get(id=int(request.POST.get('role')))
        department = Department.objects.get(id=int(request.POST.get('department')))
        print(type(first_name), middle_name, last_name, username, email, phone, password, address, gender,
              profile_picture, department, role)

        context = {'first_name': first_name, 'middle_name': middle_name, 'last_name': last_name, "username": username,
                   'email': email, 'phone': phone, 'password': password, 'address': address, 'gender': gender,
                   'role': role, 'role_list': role_list, 'department_list': department_list, 'department': department,
                   'default_password': default_password, 'existence_department_head': existence_department_head}

        # Validating the information
        employee_add_error_link = 'adminusers/employee_add.html'
        if username.strip() == "":
            messages.warning(request, 'You must have to provide an username')
            return render(request, employee_add_error_link, context)

        elif User.objects.filter(username=username).exists():
            messages.warning(request, f"Username {username} is already exists!")
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

        elif str(role) == "":
            messages.warning(request, f"Please Select a role!")
            return render(request, employee_add_error_link, context)

        else:
            # Adding user in the database
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

                user.set_password(password)

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
                            print('------------- saving data')
                            user.save()
                            print(f"{username}' is successfully added to the database.")
                            messages.success(request, f"{username} is added to the database.")
                            return redirect('employee-list')
                        else:
                            print('image is grater than 1 mb', profile_picture.size)
                            messages.error(request, 'Image size is greater than 1 mb')
                            file_system_obj.delete(profile_picture_name)
                            return render(request, 'adminusers/employee_add.html', context)
                    else:
                        print('this is not image', profile_picture.content_type)
                        messages.error(request, 'Please upload an image')
                        file_system_obj.delete(profile_picture_name)
                        return render(request, 'adminusers/employee_add.html', context)
                else:
                    print('------------- saving data without image')
                    user.save()
                    print(f"{username}'s information is successfully saved.")
                    messages.success(request, f"{username} is added.")
                    return redirect('employee-list')
            except Exception as e:
                print(e, 'exception -----------=========================================!!!!!!!!!!!!!!!!!!!')
                messages.error(request, f"Error: {e}")
                return render(request, 'adminusers/employee_add.html')
            #     return redirect('employee-list')

    return render(request, 'adminusers/employee_add.html', context)


@login_required
def employee_update(request, employee_username):
    if request.user.is_authenticated:
        print('employee is authenticated ---------')
        employee = get_object_or_404(User, username=employee_username)
        role_list = Role.objects.exclude(name__iexact='Super Admin')
        department_list = Department.objects.all()
        existence_department_head = User.objects.filter(role__name__iexact='Department Head').values_list(
            'department__name',
            flat=True)
        context = {'role_list': role_list, 'department_list': department_list, 'employee': employee,
                   'default_password': default_password, 'existence_department_head': existence_department_head}
        if request.method == "POST":
            first_name = request.POST.get('first_name')
            middle_name = request.POST.get('middle_name')
            last_name = request.POST.get('last_name')
            username = request.POST.get('username')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            password = request.POST.get('password')
            address = request.POST.get('address')
            gender = request.POST.get('gender')
            profile_picture = request.FILES.get('profile_picture')
            role = Role.objects.get(id=int(request.POST.get('role')))
            department = Department.objects.get(id=int(request.POST.get('department')))
            print(type(first_name), middle_name, last_name, username, email, phone, password, address, gender,
                  profile_picture, department, role)

            context = {'first_name': employee.first_name, 'middle_name': employee.middle_name,
                       'last_name': employee.last_name, "username": employee.username,
                       'email': employee.email, 'phone': employee.mobile_number, 'password': employee.password,
                       'address': employee.address, 'gender': employee.gender,
                       'role': employee.role, 'role_list': role_list, 'department_list': department_list,
                       'department': department, 'default_password': default_password,
                       'employee': employee, 'existence_department_head': existence_department_head}

            error_render_location = 'adminusers/employee_update.html'

            # Validating the information
            if username.strip() == "":
                messages.warning(request, 'You must have to provide an username')
                return render(request, error_render_location, context)

            elif User.objects.filter(username=username).exclude(username=employee.username).exists():

                messages.warning(request, f"Username '{username}' is already exists!")
                return render(request, error_render_location, context)

            elif email.strip() == "":
                messages.warning(request, 'You must have to provide a email!')
                return render(request, error_render_location, context)

            elif User.objects.filter(email=email).exclude(email=employee.email).exists():
                messages.warning(request, f"Email '{email}' is already exists!")
                return render(request, error_render_location, context)

            elif first_name.strip() == "":
                messages.warning(request, f"Please Provide first name!")
                return render(request, error_render_location, context)

            elif phone.strip() == "":
                messages.warning(request, f"Please Provide your phone number!")
                return render(request, error_render_location, context)

            elif gender == "":
                messages.warning(request, f"Please Provide your gender!")
                return render(request, error_render_location, context)

            elif str(role) == "":
                messages.warning(request, f"Please Select a role!")
                return render(request, error_render_location, context)

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
                    employee.role = role
                    employee.department = department
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
                                print('------------- saving data')
                                employee.save()
                                print(f"{employee.username}'s information is successfully updated.")
                                messages.success(request, f"{employee.username}'s information is updated.")
                                return redirect('employee-list')
                            else:
                                print('image is grater than 1 mb', profile_picture.size)
                                messages.error(request, 'Image size is greater than 1 mb')
                                file_system_obj.delete(profile_picture_name)
                                return render(request, 'adminusers/employee_update.html', context)
                        else:
                            print('this is not image', profile_picture.content_type)
                            messages.error(request, 'Please upload an image')
                            file_system_obj.delete(profile_picture_name)
                            return render(request, 'adminusers/employee_update.html', context)
                    else:
                        print('------------- saving data without image')
                        employee.save()
                        print(f"{employee.username}'s information is successfully updated.")
                        messages.success(request, f"{employee.username}'s information is updated.")
                        return redirect('employee-list')
                except Exception as e:
                    print(e, 'exception -----------=========================================!!!!!!!!!!!!!!!!!!!')
                    messages.error(request, f"Error: {e}")
                    return render(request, 'adminusers/employee_update.html')
                #     return redirect('employee-list')

        return render(request, 'adminusers/employee_update.html', context)


@login_required
def employee_delete(request, employee_username):
    if request.user.is_authenticated:
        user = User.objects.exclude(role__name__iexact='Super Admin')
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

        return render(request, 'adminusers/employee_list.html', context)
