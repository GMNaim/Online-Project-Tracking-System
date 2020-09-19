# members/views.py
from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.shortcuts import render, get_object_or_404, redirect

from accounts.decorators import has_access
from accounts.models import User
from adminusers.models import Task, SubmittedToQATask, user_directory_path

# Role Names

role_super_user = 'Super User'
role_admin = 'Admin'
role_department_head = 'Department Head'
role_team_leader = 'Team Leader'
role_team_member = 'Team Member'
role_employee = 'Employee'
role_tester = 'Tester'

default_password = 'test123'  # default pass
# getting user group
group_super_user = Group.objects.get(name__iexact=role_super_user)
group_admin = Group.objects.get(name__iexact=role_admin)
group_department_head = Group.objects.get(name__iexact=role_department_head)
group_team_leader = Group.objects.get(name__iexact=role_team_leader)
group_team_member = Group.objects.get(name__iexact=role_team_member)
group_employee = Group.objects.get(name__iexact=role_employee)
group_tester = Group.objects.get(name__iexact=role_tester)


@login_required(login_url='login')
@has_access(allowed_roles=[role_team_member])
def member_all_task(request):
    # user_notification_item = Module.objects.filter(
    #     assigned_team__team_member_user__username__iexact=request.user.username, status__gte=2)
    # print(user_notification_item, ' = user_notification_item')
    assigned_tasks_list_to_member = Task.objects.filter(assigned_member=request.user,
                                                        status__gte=2).order_by('-assigned_at', 'status', )
    print('assigned_tasks_list_to_member == ', assigned_tasks_list_to_member)

    """ CHANGING THE NOTIFICATION COUNT TO ZERO as he see the notification """
    current_user = User.objects.get(id=request.user.id)
    current_user.notification_count = 0
    current_user.save()

    """ LIST OF NOTIFICATION ITEMS """
    user_notification_item = Task.objects.filter(assigned_member=request.user, status=2).order_by(
        '-assigned_at', 'status')
    print('user_notification_item: -- ', user_notification_item)
    if current_user.notification_count == 0:
        user_notification_item = None

    context = {'assigned_tasks_list_to_member': assigned_tasks_list_to_member,
               'user_notification_item': user_notification_item}
    return render(request, 'members/member_all_task.html', context)


@login_required(login_url='login')
@has_access(allowed_roles=[role_team_member])
def member_task_details(request, task_id):
    if request.user.is_authenticated:
        # user_notification_item = Project.objects.filter(department_id=request.user.department.id, status=2)
        selected_task = get_object_or_404(Task, id=task_id)
        selected_task.team_member_notified = True  # as member visit detail page so he is notified
        selected_task.save()
        module_of_the_task = selected_task.module  # getting the module of the task
        print(module_of_the_task)

        """ CHANGING THE NOTIFICATION COUNT TO ZERO as he see the notification """
        current_user = User.objects.get(id=request.user.id)
        current_user.notification_count = 0
        current_user.save()

        """ LIST OF NOTIFICATION ITEMS """
        user_notification_item = Task.objects.filter(assigned_member=request.user, status=2).order_by(
            '-assigned_at', 'status')
        print('user_notification_item: -- ', user_notification_item)
        if current_user.notification_count == 0:
            user_notification_item = None

        #  If member see details of the task then team_member_notified will be true and module's status will be 3
        if selected_task.team_member_notified:
            module_of_the_task.status = 3  # if there is any task then status will be 3 means running
            module_of_the_task.save()
            selected_task.status = 3
            selected_task.save()
        context = {'selected_task': selected_task,
                   'user_notification_item': user_notification_item}
        return render(request, 'members/member_task_details.html', context)


@login_required(login_url='login')
@has_access(allowed_roles=[role_team_member])
def member_running_tasks(request):
    if request.user.is_authenticated:
        running_task = Task.objects.filter(status=3, assigned_member=request.user).order_by(
            '-assigned_at')  # 3 means running task
        context = {'running_task': running_task}
        return render(request, 'members/member_running_tasks.html', context)


@login_required(login_url='login')
@has_access(allowed_roles=[role_team_member])
def member_completed_tasks(request):
    if request.user.is_authenticated:
        completed_task = Task.objects.filter(status=5, assigned_member=request.user).order_by(
            '-assigned_at')  # 5 means completed task
        context = {'completed_task': completed_task}
        return render(request, 'members/member_completed_tasks.html', context)


@login_required(login_url='login')
@has_access(allowed_roles=[role_team_member])
def member_submitted_tasks(request):
    if request.user.is_authenticated:
        submitted_to_qa_task = Task.objects.filter(status=4, assigned_member=request.user).order_by(
            '-assigned_at')  # 4 means submitted to qa task

        context = {'submitted_to_qa_task': submitted_to_qa_task}
        return render(request, 'members/member_submitted_tasks.html', context)


@login_required(login_url='login')
@has_access(allowed_roles=[role_team_member])
def submit_task_to_qa(request, task_id):
    if request.user.is_authenticated:
        get_task = get_object_or_404(Task, id=task_id)
        testers = User.objects.filter(department__name__iexact=request.user.department.name, is_tester=True)
        print(testers)
        context = {'task': get_task, 'testers': testers}
        if request.method == 'POST':
            submitted_task_file = request.FILES.get('submitted_task_file', '')
            description = request.POST['description']
            select_tester = request.POST.get('select_tester', '')
            print(submitted_task_file, description)

            if description.strip() == "":
                context.update({'description': description})
                messages.warning(request, "Please write some description of your submitted task.")
                return render(request, 'members/submit_task.html', context)

            elif select_tester == '':
                messages.warning(request, "Please select a tester")
                return render(request, 'members/submit_task.html', context)

            else:
                """Adding submitted task in the database"""
            try:
                # this function is for saving the file under each user's folder.
                assigned_member_of_task = get_task.assigned_member.username
                user_directory_path(assigned_member_of_task, submitted_task_file)
                if select_tester != '':
                    get_tester = User.objects.get(id=select_tester)  # getting the tester obj
                submitted_task = SubmittedToQATask()
                submitted_task.tester = get_tester
                submitted_task.task = get_task
                submitted_task.description = description.strip()
                submitted_task.submitted_file = submitted_task_file
                submitted_task.save()
                # after submit the task change the task status
                get_task.status = 4  # 4 means submitted to qa team.
                get_task.is_send_tester = True
                get_task.submitted_to_tester_at = datetime.now()
                get_task.save()

                # Assign this task to the tester...
                """ Setting notification count number as task is assigned to a team member """
                # setting the notification count number as task is assigned to tester
                get_tester.notification_count += 1
                get_tester.save()
                messages.success(request, "Your task is successfully submitted to QA team.")
                return redirect('member-submitted-task')
            except Exception as e:
                print(e, 'exception -----at task submit to qa !!!')
                messages.error(request, f"Error: {e}")
                return render(request, 'members/submit_task.html')

        # submitted_to_qa_task = Task.objects.filter(status=4, assigned_member=request.user).order_by(
        #     '-assigned_at')  # 4 means submitted to qa task
        # context = {'submitted_to_qa_task': submitted_to_qa_task}
        return render(request, 'members/submit_task.html', context)


""" ==================================    TESTER WORK =              ==========================================="""


@login_required(login_url='login')
@has_access(allowed_roles=[role_tester])
def tester_all_task(request):
    # user_notification_item = Module.objects.filter(
    #     assigned_team__team_member_user__username__iexact=request.user.username, status__gte=2)
    # print(user_notification_item, ' = user_notification_item')
    tasks_list_of_tester = SubmittedToQATask.objects.filter(tester=request.user,
                                                            status=1).order_by('-created_at', 'status', )
    print('tasks_list_of_tester == ', tasks_list_of_tester)

    """ CHANGING THE NOTIFICATION COUNT TO ZERO as he see the notification """
    current_user = User.objects.get(id=request.user.id)
    current_user.notification_count = 0
    current_user.save()

    """ LIST OF NOTIFICATION ITEMS """
    user_notification_item = SubmittedToQATask.objects.filter(tester=request.user,
                                                              status=1).order_by('-created_at', 'status', )
    print('user_notification_item: -- ', user_notification_item)
    if current_user.notification_count == 0:
        user_notification_item = None

    context = {'tasks_list_of_tester': tasks_list_of_tester,
               'user_notification_item': user_notification_item}
    return render(request, 'members/tester_all_task.html', context)


@login_required(login_url='login')
@has_access(allowed_roles=[role_tester])
def tester_task_details(request, task_id):
    if request.user.is_authenticated:
        # user_notification_item = Project.objects.filter(department_id=request.user.department.id, status=2)
        selected_task = get_object_or_404(SubmittedToQATask, id=task_id)
        selected_task.tester_notified = True  # as member visit detail page so he is notified
        selected_task.save()

        """ CHANGING THE NOTIFICATION COUNT TO ZERO as he see the notification """
        current_user = User.objects.get(id=request.user.id)
        current_user.notification_count = 0
        current_user.save()

        """ LIST OF NOTIFICATION ITEMS """
        user_notification_item = SubmittedToQATask.objects.filter(tester=request.user,
                                                                  status=1).order_by('-created_at', 'status')
        print('user_notification_item: -- ', user_notification_item)
        if current_user.notification_count == 0:
            user_notification_item = None

        #  If member see details of the task then team_member_notified will be true and module's status will be 3
        if selected_task.tester_notified:
            selected_task.status = 2
            selected_task.save()
        context = {'selected_task': selected_task,
                   'user_notification_item': user_notification_item}
        return render(request, 'members/tester_task_details.html', context)


@login_required(login_url='login')
@has_access(allowed_roles=[role_tester])
def tester_running_tasks(request):
    if request.user.is_authenticated:
        running_task = Task.objects.filter(status=3, assigned_member=request.user).order_by(
            '-assigned_at')  # 3 means running task
        context = {'running_task': running_task}
        return render(request, 'members/tester_running_tasks.html', context)


@login_required(login_url='login')
@has_access(allowed_roles=[role_tester])
def tester_completed_tasks(request):
    if request.user.is_authenticated:
        completed_task = Task.objects.filter(status=5, assigned_member=request.user).order_by(
            '-assigned_at')  # 5 means completed task
        context = {'completed_task': completed_task}
        return render(request, 'members/tester_completed_tasks.html', context)
