from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse

from accounts.models import User
from projectmanager.models import Task, Module, Project

# Role Names
role_super_user = 'Super User'
role_pm = 'Project Manager'
role_department_head = 'Department Head'
role_team_leader = 'Team Leader'
role_team_member = 'Team Member'
role_employee = 'Employee'
role_tester = 'Tester'


def has_access(allowed_roles=[]):
    def decorator(view_function):
        def wrap(request, *args, **kwargs):
            request.user.role.name = str(request.user.groups.all()[0])
            if request.user.role.name in allowed_roles:
                return view_function(request, *args, **kwargs)
            else:
                return HttpResponseRedirect(reverse('dashboard'))

        return wrap

    return decorator


def has_access_dashboard(allowed_roles=[]):
    def decorator(view_function):
        def wrap(request, *args, **kwargs):
            request.user.role.name = str(request.user.groups.all()[0])
            if request.user.role.name in allowed_roles:
                return view_function(request, *args, **kwargs)
            else:
                return HttpResponseRedirect(
                    reverse('logout'))  # if not have permission to see dashboard then logout the user

        return wrap

    return decorator


# def has_access_to_assigned_task(view_function):
#     def wrap(request, *args, **kwargs):
#         task = Task.objects.filter(assigned_member=request.user)
#
#         request.user.role.name = str(request.user.groups.all()[0])
#         if request.user.role.name in allowed_roles:
#             return view_function(request, *args, **kwargs)
#         else:
#             return HttpResponseRedirect(reverse('logout'))  # if not have permission to see dashboard then logout the user
#     return wrap


from django.utils.functional import wraps


def has_access_to_assigned_task(view):
    @wraps(view)
    def inner(request, task_id, *args, **kwargs):
        # Get the task object
        task = get_object_or_404(Task, id=task_id)
        task_assigned_member = task.assigned_member
        team_leader = User.objects.get(team_member=task_assigned_member.team_member, is_team_leader=True,
                                       department=task_assigned_member.department)
        dep_head = User.objects.get(department=team_leader.department, role__name__iexact=role_department_head)
        print(team_leader, request.user, 'in decorator ************', request.user != dep_head, dep_head)
        # Check and see if task is assigned to the requested user
        if task_assigned_member != request.user and request.user != team_leader and request.user != dep_head and request.user.role.name != role_pm:
            return HttpResponseRedirect('/')

        # Return the actual company object to the view
        return view(request, task_id, *args, **kwargs)

    return inner


def has_access_to_assigned_module(view):
    """"""
    """This decorator is for to get accessed only the assigned module not other's module."""

    @wraps(view)
    def inner(request, module_id, *args, **kwargs):
        # Get the task object
        module = get_object_or_404(Module, id=module_id)
        module_assigned_leader = module.assigned_team.get_team_leader()
        dep_head = User.objects.get(department=module_assigned_leader.department,
                                    role__name__iexact=role_department_head)
        print(module_assigned_leader, request.user, dep_head, 'in decorator ************',
              request.user != module_assigned_leader)
        # Check and see if task is assigned to the requested user
        if module_assigned_leader != request.user and request.user != dep_head and request.user.role.name != role_pm:
            return HttpResponseRedirect('/')

        # Return the actual company object to the view
        return view(request, module_id, *args, **kwargs)

    return inner


def has_access_to_assigned_project(view):
    """"""
    """This decorator is for to get accessed only the assigned projects not other's project."""

    @wraps(view)
    def inner(request, project_code, *args, **kwargs):
        # Get the task object
        project = get_object_or_404(Project, code=project_code)
        project_assigned_head = project.department.employee_department.get(role__name__iexact=role_department_head)

        print(project_assigned_head, request.user, 'in decorator ************', request.user.role.name != role_pm)
        # Check and see if task is assigned to the requested user
        if project_assigned_head != request.user and request.user.role.name != role_pm:
            return HttpResponseRedirect('/')

        # Return the actual company object to the view
        return view(request, project_code, *args, **kwargs)

    return inner
