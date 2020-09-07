from django.shortcuts import render, redirect
from accounts.models import Role, User
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage

default_password = 'test123'


@login_required
def dashboard(request):
    return render(request, 'adminusers/dashboard.html')


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
    context = {'role_list': role_list, 'default_password': default_password}
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
        print(type(first_name), middle_name, last_name, username, email, phone, password, address, gender,
              profile_picture, type(role), role)

        context = {'first_name': first_name, 'middle_name': middle_name, 'last_name': last_name, "username": username,
                   'email': email, 'phone': phone, 'password': password, 'address': address, 'gender': gender,
                   'role': role, 'role_list': role_list, 'default_password': default_password}

        # Validating the information
        if username.strip() == "":
            messages.warning(request, 'You must have to provide an username')
            return render(request, 'adminusers/employee_add.html',
                          {'first_name': first_name, 'middle_name': middle_name, 'last_name': last_name,
                           'email': email, 'phone': phone, 'password': password, 'address': address, 'gender': gender,
                           'role': role, 'role_list': role_list, 'default_password': default_password})

        elif User.objects.filter(username=username).exists():
            messages.warning(request, f"Username {username} is already exists!")
            return render(request, 'adminusers/employee_add.html',
                          {'first_name': first_name, 'middle_name': middle_name, 'last_name': last_name,
                           'email': email, 'phone': phone, 'password': password, 'address': address, 'gender': gender,
                           'role': role, 'role_list': role_list, 'default_password': default_password})

        elif email.strip() == "":
            messages.warning(request, 'You must have to provide a email!')
            return render(request, 'adminusers/employee_add.html',
                          {'first_name': first_name, 'middle_name': middle_name, 'last_name': last_name,
                           "username": username,
                           'phone': phone, 'password': password, 'address': address, 'gender': gender, 'role': role,
                           'role_list': role_list, 'default_password': default_password})

        elif User.objects.filter(email=email).exists():
            messages.warning(request, f"Email {email} is already exists!")
            return render(request, 'adminusers/employee_add.html',
                          {'first_name': first_name, 'middle_name': middle_name, 'last_name': last_name,
                           "username": username,
                           'phone': phone, 'password': password, 'address': address, 'gender': gender, 'role': role,
                           'role_list': role_list, 'default_password': default_password})

        elif first_name.strip() == "":
            messages.warning(request, f"Please Provide first name!")
            return render(request, 'adminusers/employee_add.html',
                          {'middle_name': middle_name, 'last_name': last_name,
                           "username": username,
                           'email': email, 'phone': phone, 'password': password, 'address': address, 'gender': gender,
                           'role': role, 'role_list': role_list, 'default_password': default_password})

        elif phone.strip() == "":
            messages.warning(request, f"Please Provide your phone number!")
            return render(request, 'adminusers/employee_add.html',
                          {'first_name': first_name, 'middle_name': middle_name, 'last_name': last_name,
                           "username": username,
                           'email': email, 'password': password, 'address': address, 'gender': gender,
                           'role': role, 'role_list': role_list, 'default_password': default_password})

        elif gender == "":
            messages.warning(request, f"Please Provide your gender!")
            return render(request, 'adminusers/employee_add.html',
                          {'first_name': first_name, 'middle_name': middle_name, 'last_name': last_name,
                           "username": username,
                           'email': email, 'phone': phone, 'password': password, 'address': address,
                           'role': role, 'role_list': role_list, 'default_password': default_password})

        elif str(role) == "":
            messages.warning(request, f"Please Select a role!")
            return render(request, 'adminusers/employee_add.html',
                          {'first_name': first_name, 'middle_name': middle_name, 'last_name': last_name,
                           "username": username,
                           'email': email, 'phone': phone, 'password': password, 'address': address, 'gender': gender,
                           'role_list': role_list, 'default_password': default_password
                           })

        else:
            user = User.objects.create_user(first_name=first_name, middle_name=middle_name,
                                            last_name=last_name, username=username,
                                            email=email, mobile_number=phone, address=address, gender=gender, role=role)
            if profile_picture is not None:
                user.profile_picture = profile_picture
            user.set_password(password)
            user.save()
            messages.success(request, f"Employee {username} is successfully added!")
            # return render(request, 'adminusers/employee_list.html')
            return redirect('employee-list')
    return render(request, 'adminusers/employee_add.html', context)


@login_required
def employee_update(request, employee_username):
    if request.user.is_authenticated:
        print('employee is authenticated ---------')
        employee = get_object_or_404(User, username=employee_username)
        role_list = Role.objects.exclude(name__iexact='Super Admin')
        context = {'role_list': role_list, 'employee': employee, 'default_password': default_password}
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
            print(type(first_name), middle_name, last_name, username, email, phone, password, address, gender,
                  profile_picture, type(role), role)
            print('-========================================')
            print(User.objects.filter(username=username).exclude(username=employee.username).exists(),
                  '------------------username')

            context = {'first_name': employee.first_name, 'middle_name': employee.middle_name,
                       'last_name': employee.last_name, "username": employee.username,
                       'email': employee.email, 'phone': employee.mobile_number, 'password': employee.password,
                       'address': employee.address, 'gender': employee.gender,
                       'role': employee.role, 'role_list': role_list, 'default_password': default_password,
                       'employee': employee}
            error_render_location = 'adminusers/employee_update.html'

            # Validating the information
            if username.strip() == "":
                messages.warning(request, 'You must have to provide an username')
                return render(request, error_render_location, context)

            elif User.objects.filter(username=username).exclude(username=employee.username).exists():
                print(User.objects.filter(username=username), '------------------username')
                print(User.objects.filter(username=username).exclude(username=employee.username),
                      '------------------username 2')

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
                            else:
                                print('image is grater than 1 mb', profile_picture.size)
                                messages.error(request, 'Image size is greater than 1 mb')
                                file_system_obj.delete(profile_picture_name)
                                render(request, 'adminusers/employee_update.html', context)
                        else:
                            print('this is not image', profile_picture.content_type)
                            messages.error(request, 'Please upload an image')
                            file_system_obj.delete(profile_picture_name)
                            render(request, 'adminusers/employee_update.html', context)

                    employee.username = username
                    employee.email = email
                    employee.first_name = first_name
                    employee.middle_name = middle_name
                    employee.last_name = last_name
                    employee.gender = gender
                    employee.mobile_number = phone
                    employee.address = address
                    employee.role = role
                    employee.save()
                    print(f"{employee.username}'s information is successfully updated.")
                    messages.success(request, f"{employee.username}'s information is updated.")
                    redirect('employee-list')
                except Exception as e:
                    print(e, 'exception -----------=========================================!!!!!!!!!!!!!!!!!!!')
                # return render(request, 'adminusers/employee_list.html')
                return redirect('employee-list')

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
            redirect('employee-list')
        except Exception as e:
            messages.error(request, f"Error: {e}.")
            redirect('employee-list')
        return render(request, 'adminusers/employee_list.html', context)