import re

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect

# from teams.models import Membership
from .decorators import has_access
from .models import Department
from .models import User


@login_required
@has_access(allowed_roles=['Super User', 'Admin', 'Employee', 'Department Head', 'Team Leader', 'Team Member'])
def dashboard(request):
    total_employee = User.objects.filter(is_active=True).count()
    total_department = Department.objects.filter(is_active=True).count()
    context = {'total_employee': total_employee, 'total_department': total_department, 'selected': True}
    return render(request, 'adminusers/dashboard.html', context)


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

                #     Adding the user to Membership table for creating the team later.
                # membership = Membership.objects.create(user=user)
                # print('membership-------------created', membership)

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
        user = authenticate(username=employee_username, password=password)  # If user is valid then authenticte otherwise not
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
