# members/views.py
from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.forms import model_to_dict
from django.shortcuts import render, get_object_or_404, redirect

from accounts.decorators import has_access
from accounts.models import User
from projectmanager.models import Task, SubmittedToQATask, user_directory_path, TaskHistory, Module

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
    # user_notification_item = Task.objects.filter(assigned_member=request.user, status=2).order_by(
    #     '-assigned_at', 'status')
    # print('user_notification_item: -- ', user_notification_item)
    # if current_user.notification_count == 0:
    #     user_notification_item = None

    context = {'assigned_tasks_list_to_member': assigned_tasks_list_to_member,}
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

        """ CHANGING THE NOTIFICATION COUNT TO ZERO as he see the notification """
        current_user = User.objects.get(id=request.user.id)
        current_user.notification_count = 0
        current_user.save()

        """ LIST OF NOTIFICATION ITEMS """
        # user_notification_item = Task.objects.filter(assigned_member=request.user, status=2).order_by(
        #     '-assigned_at', 'status')
        # print('user_notification_item: -- ', user_notification_item)
        # if current_user.notification_count == 0:
            # user_notification_item = None

        #  If member see details of the task then team_member_notified will be true and module's status will be 3
        if selected_task.status != 7:
            if selected_task.status != 6:
                if selected_task.status != 5:
                    if selected_task.status != 4:
                        if selected_task.team_member_notified:
                            module_of_the_task.status = 3  # if there is any task then status will be 3 means running
                            module_of_the_task.save()
                            selected_task.status = 3
                            selected_task.save()

        # history of the task submitted which are verified or need modification status
        all_submitted_task_to_tester = SubmittedToQATask.objects.filter(task=selected_task, status__gt=2).order_by(
            '-created_at')
        context = {'selected_task': selected_task,
                   'all_submitted_task_to_tester': all_submitted_task_to_tester}


        """ SENDING TASK TO THE LEADER BY CLICKING THE BUTTON """
        if request.GET.get('status', None) == '7':
            if selected_task.status == 6:  # if test passed...
                try:
                    # Task completed and sending to leader
                    selected_task.status = 7  # now completed...
                    selected_task.completed_at = datetime.now()
                    selected_task.is_send_to_leader = True
                    selected_task.save()

                    """ Setting notification count number as completed task is send to team leader """
                    # getting the team leader
                    task_send_to_team_leader = User.objects.get(team_member=module_of_the_task.assigned_team,
                                                                role__name__exact=role_team_leader)
                    print(task_send_to_team_leader)
                    # setting the notification count number as task is completed
                    task_send_to_team_leader.notification_count += 1
                    task_send_to_team_leader.save()
                    # print(task_send_to_team_leader.id, 'ddddddddddddddddd')

                    # create new task history object as task is completed
                    task_history = TaskHistory()
                    task_history.task = selected_task
                    task_history.module = module_of_the_task
                    task_history.description = (model_to_dict(selected_task))
                    task_history.status = 'Task Completed'
                    task_history.user = task_send_to_team_leader
                    task_history.save()




                    """ =============Checking whether the Module is completed ============="""
                    task_list = Task.objects.filter(module=module_of_the_task)
                    all_task = task_list.count()
                    task_complete_counter = 0
                    print(task_list, all_task)

                    for task in task_list:
                        print(task.get_status_display())
                        if task.status == 7:
                            task_complete_counter += 1  # if task is completed then increment then compare it with total task.

                    module_of_the_task.progress = (task_complete_counter / all_task) * 100   # progress of the module...
                    module_of_the_task.save()
                    print(module_of_the_task.progress, '% == progress of the module....')

                    if all_task == task_complete_counter:
                        module_of_the_task.status = 4
                        module_of_the_task.is_completed = True
                        module_of_the_task.completed_at = datetime.now()
                        module_of_the_task.save()



                        """ Setting notification for head as the module is completed. """
                        # getting the head
                        head_of_the_dep = User.objects.get(department=request.user.department, role__name__iexact=role_department_head)
                        print('head_of_the_dep: ', head_of_the_dep)
                        # setting the notification count number as task is completed
                        head_of_the_dep.notification_count += 1
                        head_of_the_dep.save()

                        # create new task history object as module is completed
                        task_history = TaskHistory()
                        task_history.module = module_of_the_task
                        task_history.project = module_of_the_task.project
                        task_history.description = (model_to_dict(module_of_the_task))
                        task_history.status = 'Module Completed'
                        task_history.user = head_of_the_dep
                        task_history.save()

                    else:
                        module_of_the_task.is_completed = False
                        module_of_the_task.status = 3
                        module_of_the_task.completed_at = None
                        module_of_the_task.save()
                    print('---------.///', module_of_the_task.name, module_of_the_task.get_status_display())


                    """ =============Checking whether the Project is completed ============="""
                    project_of_the_modules = module_of_the_task.project  # getting the project of the tasks/modules
                    print(project_of_the_modules)
                    list_of_modules_of_a_project = Module.objects.filter(project=project_of_the_modules)  # all module of the project
                    total_modules_of_a_project = list_of_modules_of_a_project.count()
                    print(total_modules_of_a_project)
                    module_complete_counter = 0

                    for module in list_of_modules_of_a_project:
                        print(module.get_status_display())
                        if module.status == 4:
                            module_complete_counter += 1  # if module is completed then increment then compare it with total task.

                    if total_modules_of_a_project == module_complete_counter:
                        project_of_the_modules.status = 4
                        print(project_of_the_modules.get_status_display(), 'showing status after setting 4')
                        # project_of_the_modules.is_completed = True
                        project_of_the_modules.completed_at = datetime.now()
                        project_of_the_modules.save()


                        """ Setting notification for pm as the module is completed. """
                        # getting the project manager
                        all_pm = User.objects.filter(role__name__iexact=role_pm)
                        pm = project_of_the_modules.assigned_by
                        print('All pm are: : ', pm, all_pm)

                        for p_m in all_pm:
                            # setting the notification count number as task is completed
                            p_m.notification_count += 1
                            p_m.save()
                            # create new task history object as module is completed
                            task_history = TaskHistory()
                            task_history.project = project_of_the_modules
                            task_history.description = (model_to_dict(project_of_the_modules))
                            task_history.status = 'Project Completed'
                            task_history.user = p_m
                            task_history.save()

                    else:
                        # project_of_the_modules.is_completed = False
                        project_of_the_modules.status = 3
                        print(project_of_the_modules.get_status_display(), 'showing status in else...')
                        project_of_the_modules.completed_at = None
                        project_of_the_modules.save()

                    print('---------.///', module_of_the_task.name, module_of_the_task.get_status_display())




                    messages.success(request, f"Congratulation! You have completed the task. Task Send to Team Leader.")
                    return redirect('member-completed-task')
                except Exception as e:
                    print('error at task send to leader...', e)
                    return render(request, 'members/member_task_details.html', context)



        # task_history = TaskHistory.objects.filter(task=selected_task)
        # print(task_history)

        return render(request, 'members/member_task_details.html', context)


@login_required(login_url='login')
@has_access(allowed_roles=[role_team_member])
def member_running_tasks(request):
    if request.user.is_authenticated:
        running_task = Task.objects.filter(status__in=[3], assigned_member=request.user).order_by(
            '-assigned_at')  # 3 means running task
        context = {'running_task': running_task}
        return render(request, 'members/member_running_tasks.html', context)


@login_required(login_url='login')
@has_access(allowed_roles=[role_team_member])
def member_test_passed_tasks(request):
    if request.user.is_authenticated:
        completed_task = Task.objects.filter(status=6, assigned_member=request.user).order_by(
            '-assigned_at')  # 5 means completed task
        context = {'completed_task': completed_task}
        return render(request, 'members/member_test_passed_tasks.html', context)


@login_required(login_url='login')
@has_access(allowed_roles=[role_team_member])
def member_completed_tasks(request):
    if request.user.is_authenticated:
        completed_task = Task.objects.filter(status=7, assigned_member=request.user).order_by(
            '-assigned_at')  # 5 means completed task
        context = {'completed_task': completed_task}
        print(completed_task, '3333333333333333')
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
def submit_task_to_tester(request, task_id):
    if request.user.is_authenticated:
        get_task = get_object_or_404(Task, id=task_id)
        testers = User.objects.filter(department__name__iexact=request.user.department.name, is_tester=True)
        print(testers)
        last_submitted_task = []
        print(get_task.submittedtoqatask_set.all().count())
        if get_task.submittedtoqatask_set.all().count() != 0:
            last_submitted_task = SubmittedToQATask.objects.filter(task=get_task).last()
            print(last_submitted_task, '8888888')
        print(last_submitted_task, '8888888')
        context = {'task': get_task, 'testers': testers, 'last_submitted_task': last_submitted_task}
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
                """Adding submitted task in the SubmittedToQATask model"""
            try:
                # this function is for saving the file under each user's folder.
                assigned_member_of_task = get_task.assigned_member.username
                user_directory_path(assigned_member_of_task, submitted_task_file)
                if select_tester != '':
                    get_tester = User.objects.get(id=select_tester)  # getting the tester obj

                submitted_task = SubmittedToQATask()
                submitted_task.assigned_member = get_tester
                submitted_task.task = get_task
                submitted_task.description = description.strip()
                submitted_task.submitted_file = submitted_task_file
                submitted_task.save()

                # after submit the task change the task status
                get_task.status = 4  # 4 means submitted to qa team.
                get_task.is_send_tester = True
                get_task.submitted_to_tester_at = datetime.now()
                # making team_member_notified false cause to get the color of the new notification item.
                get_task.team_member_notified = False
                get_task.save()

                # create new task history object
                task_history = TaskHistory()
                # task_history.task = get_task
                task_history.submitted_task = submitted_task
                task_history.task = get_task
                task_history.description = (model_to_dict(get_task))
                task_history.status = 'New Task'
                task_history.user = get_tester
                task_history.save()

                # Assign this task to the tester...
                """ Setting notification count number as task is send to a tester """
                # setting the notification count number as task is assigned to tester
                get_tester.notification_count += 1
                get_tester.save()
                messages.success(request, "Your task is successfully submitted to tester.")
                return redirect('member-submitted-task')
            except Exception as e:
                print(e, 'exception -----at task submit to qa !!!')
                messages.error(request, f"Error: {e}")
                return render(request, 'members/submit_task.html')

        # submitted_to_qa_task = Task.objects.filter(status=4, assigned_member=request.user).order_by(
        #     '-assigned_at')  # 4 means submitted to qa task
        # context = {'submitted_to_qa_task': submitted_to_qa_task}
        return render(request, 'members/submit_task.html', context)


@login_required(login_url='login')
@has_access(allowed_roles=[role_team_member])
def member_need_modification_tasks(request):
    if request.user.is_authenticated:
        need_modification_task = Task.objects.filter(status=5, assigned_member=request.user).order_by(
            '-assigned_at')  # 3 means running task
        # fix_bug_tasks = SubmittedToQATask.objects.filter(task__assigned_member=request.user, status=3).order_by(
        #     '-verified_at')
        context = {'need_modification_task': need_modification_task}
        return render(request, 'members/member_need_modification_tasks.html', context)


# #
# @login_required(login_url='login')
# @has_access(allowed_roles=[role_team_member])
# def member_task_send_to_leader(request, task_id):
#     if request.user.is_authenticated:
        #         selected_task = get_object_or_404(Task, id=task_id)
        #         # module_of_the_task = selected_task.module  # getting the module of the task
        #         # current_user = User.objects.get(id=request.user.id)
        #         # current_user.notification_count = 0
        #         # current_user.save()
        #         # if current_user.notification_count == 0:
        #         #     user_notification_item = None
        #         #
        #         # #  If member see details of the task then team_member_notified will be true and module's status will be 3
        #         # if selected_task.status != 6:
        #         #     if selected_task.status != 5:
        #         #         if selected_task.status != 4:
        #         #             if selected_task.team_member_notified:
        #         #                 module_of_the_task.status = 3  # if there is any task then status will be 3 means running
        #         #                 module_of_the_task.save()
        #         #                 selected_task.status = 3
        #         #                 selected_task.save()
        #
        #
        #         # history of the task submitted which are verified or need modification status
        #         all_submitted_task_to_tester = SubmittedToQATask.objects.filter(task=selected_task, status__gt=2).order_by(
        #             '-created_at')
        #         context = {'selected_task': selected_task,
        #                    'all_submitted_task_to_tester': all_submitted_task_to_tester}
        #
        #
        #             except Exception as e:
        #                 print('error at task send to leader...', e)
        #                 return render(request, 'members/member_task_details.html', context)
        #
        # return render(request, 'members/member_task_details.html')


#


""" ==================================    TESTER WORK =              ==========================================="""


@login_required(login_url='login')
@has_access(allowed_roles=[role_tester])
def tester_all_task(request):
    # user_notification_item = Module.objects.filter(
    #     assigned_team__team_member_user__username__iexact=request.user.username, status__gte=2)
    # print(user_notification_item, ' = user_notification_item')
    tasks_list_of_tester = SubmittedToQATask.objects.filter(assigned_member=request.user).order_by('-created_at', )
    # print('tasks_list_of_tester == ', tasks_list_of_tester)

    """ CHANGING THE NOTIFICATION COUNT TO ZERO as he see the notification """
    current_user = User.objects.get(id=request.user.id)
    current_user.notification_count = 0
    current_user.save()

    """ LIST OF NOTIFICATION ITEMS """
    # user_notification_item = SubmittedToQATask.objects.filter(assigned_member=request.user,
    #                                                           status=1).order_by('-created_at', 'status', )

    # if current_user.notification_count == 0:
    #     user_notification_item = None

    context = {'tasks_list_of_tester': tasks_list_of_tester}
    return render(request, 'members/tester_all_task.html', context)


@login_required(login_url='login')
@has_access(allowed_roles=[role_tester])
def tester_task_details(request, task_id):
    if request.user.is_authenticated:
        # user_notification_item = Project.objects.filter(department_id=request.user.department.id, status=2)
        selected_task = get_object_or_404(SubmittedToQATask, id=task_id)
        actual_task = selected_task.task  # actual task send by the developer or team member
        developer_of_actual_task = selected_task.task.assigned_member  # developer or team member
        selected_task.tester_notified = True  # as member visit detail page so he is notified
        selected_task.save()

        list_of_same_tasks = SubmittedToQATask.objects.filter(task_id=actual_task.id)
        print(list_of_same_tasks, '-------.....')

        """ CHANGING THE NOTIFICATION COUNT TO ZERO as he see the notification """
        current_user = User.objects.get(id=request.user.id)
        current_user.notification_count = 0
        current_user.save()

        """ LIST OF NOTIFICATION ITEMS """
        # user_notification_item = SubmittedToQATask.objects.filter(assigned_member=request.user,
        #                                                           status=1).order_by('-created_at', 'status')
        # print('user_notification_item: -- ', user_notification_item)
        # if current_user.notification_count == 0:
        #     user_notification_item = None

        #  If member see details of the task then team_member_notified will be true and module's status will be 3
        if selected_task.status != 4:
            if selected_task.status != 3:
                if selected_task.tester_notified:
                    selected_task.status = 2
                    selected_task.save()

        context = {'selected_task': selected_task}

        if request.method == "POST":
            bug_suggestion = request.POST.get('bug_suggestion', '')
            if 'submit_bug' in request.POST:
                if bug_suggestion.strip() == '':
                    messages.warning(request, 'You are submitting as "fix bug" but didn\'t tell any suggestion.')
                    return render(request, 'members/tester_task_details.html', context)
                else:
                    try:
                        print(bug_suggestion, 'bug_suggestion')
                        selected_task.bug = bug_suggestion
                        selected_task.has_bug = True
                        selected_task.status = 3
                        selected_task.is_verified = True
                        selected_task.verified_at = datetime.now()
                        selected_task.save()

                        actual_task.status = 5  # actual task  need modification as has bug
                        actual_task.save()

                        # if task's status=3 then other copy of the same task
                        # which is submitted before those task's  status = 3.
                        # for task in list_of_same_tasks:
                        #     task.status = 3
                        #     task.save()

                        # create new task history object
                        task_history = TaskHistory()
                        task_history.task = actual_task
                        task_history.description = (model_to_dict(actual_task))
                        task_history.status = 'Need Modification'
                        task_history.user = developer_of_actual_task
                        task_history.save()
                        # setting the notification count number as task is done and send to the developer again
                        developer_of_actual_task.notification_count += 1
                        developer_of_actual_task.save()
                        messages.success(request, f"{selected_task} is send back to developer to fix bug.")
                    except Exception as e:
                        print('Error at tester submit bug feedback', e)

            else:
                try:
                    print(bug_suggestion, 'bug_suggestion')
                    if bug_suggestion != '':  # otherwise get default value
                        selected_task.bug = bug_suggestion
                    selected_task.has_bug = False
                    selected_task.status = 4
                    selected_task.is_verified = True
                    selected_task.verified_at = datetime.now()
                    selected_task.save()
                    actual_task.status = 6  # actual task is now completed as no bug
                    # actual_task.completed_at = datetime.now()
                    actual_task.save()
                    # if task is completed/ verified then other copy of the same task
                    # which is submitted before those also will be completed/verified.
                    # for task in list_of_same_tasks:
                    #     task.status = 4
                    #     task.save()
                    # create new task history object
                    task_history = TaskHistory()
                    task_history.task = actual_task
                    task_history.description = (model_to_dict(actual_task))
                    task_history.status = 'Worked Done'
                    task_history.user = developer_of_actual_task
                    task_history.save()
                    # setting the notification count number as task is done and send to the developer again
                    developer_of_actual_task.notification_count += 1
                    developer_of_actual_task.save()
                    # user_notification_item =
                    messages.success(request, f"{selected_task} is send back to developer as verified.")
                    return redirect('tester-completed-task')
                except Exception as e:
                    print('Error at tester submit feedback', e)

        return render(request, 'members/tester_task_details.html', context)


@login_required(login_url='login')
@has_access(allowed_roles=[role_tester])
def tester_running_tasks(request):
    if request.user.is_authenticated:
        running_tasks_list_of_tester = SubmittedToQATask.objects.filter(assigned_member=request.user,
                                                                        status=2).order_by(
            '-created_at', 'status', )
        running_tasks_count_of_tester = running_tasks_list_of_tester.count()
        print('running_tasks_list_of_tester == ', running_tasks_list_of_tester)
        context = {'running_tasks_list_of_tester': running_tasks_list_of_tester,
                   'running_tasks_count_of_tester': running_tasks_count_of_tester}
        return render(request, 'members/tester_running_tasks.html', context)


@login_required(login_url='login')
@has_access(allowed_roles=[role_tester])
def tester_completed_tasks(request):
    if request.user.is_authenticated:
        completed_tasks_list_of_tester = SubmittedToQATask.objects.filter(assigned_member=request.user,
                                                                          status=4).order_by(
            '-created_at', 'status', )
        completed_tasks_count_of_tester = completed_tasks_list_of_tester.count()
        print('running_tasks_list_of_tester == ', completed_tasks_list_of_tester)
        context = {'running_tasks_list_of_tester': completed_tasks_list_of_tester,
                   'completed_tasks_count_of_tester': completed_tasks_count_of_tester}
        return render(request, 'members/tester_completed_tasks.html', context)
