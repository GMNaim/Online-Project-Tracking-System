from django.shortcuts import render
from accounts.models import Role, User
from django.contrib import messages


def dashboard(request):
    role = Role.objects.all()
    role_admin = str(request.user.role).lower()
    print(str(request.user.role).lower(), '========================')
    if role_admin == 'admin':
        context = {'admin': role_admin}
        return render(request, 'adminusers/dashboard.html', context)
    return render(request, 'base/base_template.html')


def client_list(request):
    return render(request, 'adminusers/client_list.html')


def client_add(request):
    return render(request, 'adminusers/client_add.html')


def project_add(request):
    return render(request, 'adminusers/project_add.html')


def project_list(request):
    return render(request, 'adminusers/project_list.html')


def employee_list(request):
    user = User.objects.exclude(role__name__iexact='Super Admin')
    print(user, '-------------')
    for user in user:
        print(user.is_superuser, user.is_staff, user)

    return render(request, 'adminusers/employee_list.html')


def employee_add(request):
    user = User.objects.all()
    role_list = Role.objects.exclude(name__iexact='Super Admin')
    print(role_list, '-----------------------------')
    context = {'role_list': role_list}
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        middle_name = request.POST.get('middle_name', '-m name')
        last_name = request.POST.get('last_name', '- l name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        address = request.POST.get('address', '-address')
        gender = request.POST.get('gender', '-gender')
        profile_picture = request.FILES.get('profile_picture')
        role = request.POST.get('role', '---role')
        print(type(first_name), middle_name, last_name, username, email, phone, password, address, gender, profile_picture,
              role)

        context = {'first_name': first_name, 'middle_name': middle_name, 'last_name': last_name, "username": username,
                   'email': email, 'phone': phone, 'password': password, 'address': address, 'gender': gender,
                   'role': role, 'role_list': role_list}

        # Validating the information
        if username.strip() == "":
            messages.warning(request, 'You must have to provide an email')
            return render(request, 'adminusers/employee_add.html',
                          {'first_name': first_name, 'middle_name': middle_name, 'last_name': last_name,
                           'email': email, 'phone': phone, 'password': password, 'address': address, 'gender': gender,
                           'role': role, 'role_list': role_list})

        elif User.objects.filter(username=username).exists():
            messages.warning(request, f"Username {username} is already exists!")
            return render(request, 'adminusers/employee_add.html',
                          {'first_name': first_name, 'middle_name': middle_name, 'last_name': last_name,
                           'email': email, 'phone': phone, 'password': password, 'address': address, 'gender': gender,
                           'role': role, 'role_list': role_list})

        elif email.strip() == "":
            messages.warning(request, 'You must have to provide a username!')
            return render(request, 'adminusers/employee_add.html',
                          {'first_name': first_name, 'middle_name': middle_name, 'last_name': last_name,
                           "username": username,
                           'phone': phone, 'password': password, 'address': address, 'gender': gender, 'role': role, 'role_list': role_list})

        elif User.objects.filter(email=email).exists():
            messages.warning(request, f"Email {email} is already exists!")
            return render(request, 'adminusers/employee_add.html',
                          {'first_name': first_name, 'middle_name': middle_name, 'last_name': last_name,
                           "username": username,
                           'phone': phone, 'password': password, 'address': address, 'gender': gender, 'role': role, 'role_list': role_list})

        elif first_name.strip() == "":
            messages.warning(request, f"Please Provide first name!")
            return render(request, 'adminusers/employee_add.html',
                          {'middle_name': middle_name, 'last_name': last_name,
                           "username": username,
                           'email': email, 'phone': phone, 'password': password, 'address': address, 'gender': gender,
                           'role': role, 'role_list': role_list})

        elif phone.strip() == "":
            messages.warning(request, f"Please Provide your phone number!")
            return render(request, 'adminusers/employee_add.html',
                          {'first_name': first_name, 'middle_name': middle_name, 'last_name': last_name,
                           "username": username,
                           'email': email, 'password': password, 'address': address, 'gender': gender,
                           'role': role, 'role_list': role_list})

        elif gender == "":
            messages.warning(request, f"Please Provide your gender!")
            return render(request, 'adminusers/employee_add.html',
                          {'first_name': first_name, 'middle_name': middle_name, 'last_name': last_name,
                           "username": username,
                           'email': email, 'phone': phone, 'password': password, 'address': address,
                           'role': role, 'role_list': role_list})

        elif role == "":
            messages.warning(request, f"Please Select a role!")
            return render(request, 'adminusers/employee_add.html',
                          {'first_name': first_name, 'middle_name': middle_name, 'last_name': last_name,
                           "username": username,
                           'email': email, 'phone': phone, 'password': password, 'address': address, 'gender': gender, 'role_list': role_list
                           })

        return render(request, 'adminusers/employee_list.html', context)

    return render(request, 'adminusers/employee_add.html', context)
