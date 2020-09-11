from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from .models import Department
from accounts.decorators import has_access

@login_required
@has_access(allowed_roles=['Admin', 'Super User'])
def department_list(request):
    department = Department.objects.all()

    # for d in department:
    #     print(d.get_department_info())
    #     print(d.name, d.get_total_employee(), 'total employee----')

    context = {'department': department, 'not_assigned': 'Not Assigned'}
    return render(request, 'departments/department_list.html', context)


@login_required
@has_access(allowed_roles=['Admin', 'Super User'])
def department_add(request):
    if request.user.is_authenticated:

        department = Department.objects.all()

        context = {'department': department, 'not_assigned': 'Not Assigned'}
        if request.method == "POST":
            name = request.POST['name']
            description = request.POST['description']
            context['description'] = description
            context['name'] = name
            if str(name).strip() == "":
                messages.warning(request, 'You must have to give department name!')
                return render(request, 'departments/department_add.html', context)

            elif Department.objects.filter(name__iexact=name).exists():
                messages.warning(request, f"'Department {name}' is already exists!")
                return render(request, 'departments/department_add.html', context)

            else:
                try:
                    # new_department = Department()  # creating obj of department
                    # new_department.name = name
                    # new_department.description = description
                    # new_department.save()
                    Department.objects.create(name=name, description=description)
                    messages.success(request, 'Department added! Please assign a department head.')
                    print('department added--------------')
                    # return render(request, 'departments/department_list.html', context)
                    return redirect('department-list')
                except Exception as e:
                    print(e)
                    messages.error(request, f"Error: {e}")
                    return render(request, 'departments/department_add.html', context)
        return render(request, 'departments/department_add.html', context)


@login_required
@has_access(allowed_roles=['Admin', 'Super User'])
def department_update(request, department_name):
    if request.user.is_authenticated:
        selected_department = get_object_or_404(Department, name=department_name)
        department = Department.objects.all()

        context = {'department': department, 'not_assigned': 'Not Assigned', 'selected_department': selected_department}
        if request.method == "POST":
            name = request.POST['name']
            description = request.POST['description']
            context['description'] = description
            context['name'] = name
            if str(name).strip() == "":
                messages.warning(request, 'You must have to give department name!')
                return render(request, 'departments/department_update.html', context)

            elif Department.objects.filter(name__iexact=name).exclude(name__iexact=selected_department.name).exists():
                messages.warning(request, f"'Department {name}' is already exists!")
                return render(request, 'departments/department_update.html', context)

            else:
                try:
                    selected_department.name = name
                    selected_department.description = description
                    selected_department.save()
                    messages.success(request,
                                     f'Department "{selected_department.name}" is Updated!')
                    print('department added--------------')
                    # return render(request, 'departments/department_list.html', context)
                    return  redirect('department-list')
                except Exception as e:
                    print(e)
                    messages.error(request, f"Error: {e}")
                    return render(request, 'departments/department_update.html', context)
        return render(request, 'departments/department_update.html', context)


@login_required
@has_access(allowed_roles=['Admin', 'Super User'])
def department_delete(request, department_name):
    if request.user.is_authenticated:
        department = Department.objects.all()
        selected_department = get_object_or_404(Department, name=department_name)

        context = {'department': department, 'not_assigned': 'Not Assigned', 'selected_department': selected_department}
        try:
            selected_department.delete()
            messages.success(request, f"Department '{selected_department.name}' is deleted!")
            return redirect('department-list')
        except selected_department.DoesNotExist:
            messages.error(request, 'Department does not exist')
            return redirect('department-list')
        except Exception as e:
            messages.error(request, f"Error: {e}.")
        return render(request, 'departments/department_list.html', context)
