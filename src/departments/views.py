from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.forms import model_to_dict
from django.shortcuts import render, get_object_or_404, redirect

from accounts.decorators import has_access, has_access_to_assigned_project
from accounts.models import User
from projectmanager.models import Project, Module, TaskHistory
from teams.models import Team
from .models import Department

# Role Names
role_super_user = 'Super User'
role_pm = 'Project Manager'
role_department_head = 'Department Head'
role_team_leader = 'Team Leader'
role_team_member = 'Team Member'
role_employee = 'Employee'

default_password = 'test123'  # default pass
# getting user group
group_super_user = Group.objects.get(name__iexact=role_super_user)
group_pm = Group.objects.get(name__iexact=role_pm)
group_department_head = Group.objects.get(name__iexact=role_department_head)
group_team_leader = Group.objects.get(name__iexact=role_team_leader)
group_team_member = Group.objects.get(name__iexact=role_team_member)
group_employee = Group.objects.get(name__iexact=role_employee)


@login_required(login_url='login')
@has_access(allowed_roles=[role_pm, role_super_user])
def department_list(request):
    department = Department.objects.all()

    # for d in department:
    #     print(d.get_department_info())
    #     print(d.name, d.get_total_employee(), 'total employee----')

    context = {'department': department, 'not_assigned': 'Not Assigned'}
    return render(request, 'departments/department_list.html', context)


@login_required(login_url='login')
@has_access(allowed_roles=[role_pm, role_super_user])
def department_add(request):
    if request.user.is_authenticated:

        department = Department.objects.all()

        context = {'department': department, 'not_assigned': 'Not Assigned'}
        if request.method == "POST":
            name = str(request.POST.get('name')).strip()
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


@login_required(login_url='login')
@has_access(allowed_roles=[role_pm, role_super_user])
def department_update(request, department_name):
    if request.user.is_authenticated:
        selected_department = get_object_or_404(Department, name=department_name)
        department = Department.objects.all()

        context = {'department': department, 'not_assigned': 'Not Assigned', 'selected_department': selected_department}
        if request.method == "POST":
            name = str(request.POST['name']).strip()
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
                    return redirect('department-list')
                except Exception as e:
                    print(e)
                    messages.error(request, f"Error: {e}")
                    return render(request, 'departments/department_update.html', context)
        return render(request, 'departments/department_update.html', context)


@login_required(login_url='login')
@has_access(allowed_roles=[role_pm, role_super_user])
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


"""=======================================   DEPARTMENT HEAD PART    ============================================="""


@login_required(login_url='login')
@has_access(allowed_roles=[role_department_head])
def department_all_project(request):
    assigned_projects_list_to_head = Project.objects.filter(department_id=request.user.department.id,
                                                            status__gte=2).order_by('-assigned_at')
    """ CHANGING THE NOTIFICATION COUNT TO ZERO """
    # current_user = User.objects.get(id=request.user.id)
    # current_user.notification_count = 0
    # current_user.save()
    """ LIST OF NOTIFICATION ITEMS """
    # user_notification_item = Project.objects.filter(department_id=request.user.department.id,
    #                                                    status=2).order_by('-assigned_at', 'status')
    # if current_user.notification_count == 0:  # if notification count zero then notification items none.
    #     user_notification_item = None

    context = {'assigned_projects_list_to_head': assigned_projects_list_to_head}
    return render(request, 'departments/department_all_project.html', context)


@login_required(login_url='login')
@has_access(allowed_roles=[role_department_head])
def department_running_project(request):
    dep_running_project = Project.objects.filter(department=request.user.department, status=3)

    context = {'dep_running_project': dep_running_project, }
    return render(request, 'departments/department_running_project.html', context)


@login_required(login_url='login')
@has_access(allowed_roles=[role_department_head])
def department_completed_project(request):
    dep_completed_project = Project.objects.filter(department=request.user.department, status=4)
    print(dep_completed_project, '-----------------------77777777')

    context = {'dep_completed_project': dep_completed_project, }
    return render(request, 'departments/department_completed_project.html', context)


@login_required(login_url='login')
@has_access(allowed_roles=[role_department_head, role_pm])
@has_access_to_assigned_project
def department_project_details(request, project_code):
    # user_notification_item = Project.objects.filter(department_id=request.user.department.id, status=2)
    selected_project = get_object_or_404(Project, code=project_code)
    selected_project.department_head_notified = True  # if head visit project detail page that means he is notified.
    selected_project.save()
    module_list = Module.objects.filter(project=selected_project)  # module list of the selected project
    print(module_list.count())
    #  If there is at least one module created then project status will be change to running.
    # if selected_project.status != 4 and module_list.count() > 0:
    if module_list.count() > 0:
        selected_project.status = 3  # if any module then status will be 3 means running
        selected_project.save()
        # selected_project.save()
        #  if all task's status is 7 then project is completed... below code is for that
        print(module_list)
        # module_complete_count = 0
        # for module in module_list:
        #     # print(module.status, 'in for....')
        #     if module.status == 4:
        #         module_complete_count += 1

        total_task = 0
        task_complete_counter = 0
        for module in module_list:
            # total_task += module.task_set.all().count()
            for task in module.task_set.all():
                total_task += 1
                if task.status == 7:
                    task_complete_counter += 1

        print(f'total task of the project {selected_project.name} is : ====== ', total_task)
        # changing the status of the project based on task completion
        if total_task > 0 and total_task == task_complete_counter:
            selected_project.status = 4
            selected_project.completed_at = datetime.now()
            selected_project.save()

        if total_task != 0:
            selected_project.progress = int((task_complete_counter / total_task) * 100)   # progress of the project
            selected_project.save()
        print(selected_project.progress, '% == progress of the project....')

        # if module_list.count() == module_complete_count:
        #     selected_project.status = 4
        #     selected_project.save()


    """ CHANGING THE NOTIFICATION COUNT TO ZERO as he see the notification"""
    # current_user = User.objects.get(id=request.user.id)
    # current_user.notification_count = 0
    # current_user.save()

    """ LIST OF NOTIFICATION ITEMS making zero as he see the notification... """
    # user_notification_item = Project.objects.filter(department_id=request.user.department.id,
    #                                                 status=2).order_by('-assigned_at', 'status')
    # if current_user.notification_count == 0:  # if notification count zero then notification items none.
    #     user_notification_item = None

    context = {'selected_project': selected_project,
               'module_list': module_list}
    return render(request, 'departments/department_project_details.html', context)


@login_required(login_url='login')
@has_access(allowed_roles=[role_department_head])
def module_create(request, project_code):
    if request.user.is_authenticated:
        selected_project = get_object_or_404(Project, code=project_code)
        team_in_dep = Team.objects.filter(team_member_user__department_id=request.user.department.id).exclude(
            id=10).distinct()  # getting all team of signed in department head's department
        print(team_in_dep)
        print(selected_project.delivery_date, type(selected_project.delivery_date),
              selected_project.delivery_date.day > 0)
        context = {'selected_project': selected_project, 'team_in_department': team_in_dep}

        if request.method == "POST":
            name = str(request.POST['name']).strip()
            selected_team = request.POST['select_team']
            description = request.POST['description']
            submission_date = request.POST['submission_date']
            print('Post data: = ', name, selected_team, description, submission_date)

            date_obj = datetime.strptime(submission_date, '%Y-%m-%d')  # converting string date to date obj
            submission_date_obj = date_obj.date()  # datetime obj to save in model
            print('Date:', submission_date_obj)
            today = datetime.today().date()
            print(today)
            check_old_date = submission_date_obj - today  # checking whether given date is old than today
            print(check_old_date)
            context = {'team_in_department': team_in_dep,
                       'name': name,
                       'description': description,
                       'selected_team': int(selected_team),
                       'submission_date': submission_date_obj.strftime("%Y-%m-%d"),
                       'selected_project': selected_project, }
            # Validating the information
            module_add_error_link = 'departments/module_add.html'
            if check_old_date.days < 0:
                messages.warning(request, 'Please select a valid submission date.')
                return render(request, module_add_error_link, context)

            elif name.strip() == "":
                messages.warning(request, 'Please provide a project name')
                return render(request, module_add_error_link, context)

            elif Module.objects.filter(name__iexact=name).exists():
                messages.warning(request, 'There is another module with this name. Please change the name.')
                return render(request, module_add_error_link, context)

            elif description.strip() == "":
                messages.warning(request, 'Please provide detail description of the module.')
                return render(request, module_add_error_link, context)

            elif selected_team == '':
                messages.warning(request, f"Please select a team!")
                return render(request, module_add_error_link, context)

            elif submission_date == '':
                messages.warning(request, f"Please provide submission date!")
                return render(request, module_add_error_link, context)

            elif submission_date_obj > selected_project.delivery_date:
                messages.warning(request,
                                 f"Project delivery date is {selected_project.delivery_date}."
                                 f" But you set submission date {submission_date_obj}!")
                return render(request, module_add_error_link, context)

            else:
                try:
                    #  Saving data to database

                    selected_team_obj = Team.objects.get(id=int(selected_team))  # getting the team obj.
                    module = Module(name=name,  # creating a new module
                                    description=description,
                                    assigned_team=selected_team_obj,
                                    project=selected_project,
                                    submission_date=submission_date_obj)
                    module.save()  # saving new created module
                    print(module.project.name)
                    # #  If there is at least one module created then project status will be change to running.
                    # if selected_project.module_set.all().count() > 0:
                    #     selected_project.status = 3  # if any module then status will be 3 means nunning
                    #     selected_project.save()
                    messages.success(request, f"Module '{name}' is created successfully!")
                    return redirect('department-project-details', project_code=selected_project.code)
                except Exception as e:
                    print(e)
                    messages.error(request, e)
                    return render(request, module_add_error_link, context)

        return render(request, 'departments/module_add.html', context)


@login_required(login_url='login')
@has_access(allowed_roles=[role_department_head])
def module_update(request, project_code, module_id):
    if request.user.is_authenticated:
        selected_project = get_object_or_404(Project, code=project_code)  # getting the selected project
        selected_module = get_object_or_404(Module, id=module_id)  # getting the selected module
        team_in_dep = Team.objects.filter(team_member_user__department_id=request.user.department.id).exclude(
            id=10).distinct()  # getting all team of signed in department head's department
        print(team_in_dep)
        print(selected_project.delivery_date, type(selected_project.delivery_date),
              selected_project.delivery_date.day > 0)
        context = {'selected_project': selected_project,
                   'team_in_department': team_in_dep,
                   'selected_module': selected_module,
                   'name': selected_module.name,
                   'description': selected_module.description,
                   'submission_date': selected_module.submission_date.strftime("%Y-%m-%d"),
                   'module_status': selected_module.status}

        if request.method == "POST":
            name = str(request.POST['name']).strip()
            selected_team = request.POST['select_team']
            description = request.POST['description']
            submission_date = request.POST['submission_date']
            module_status = request.POST.get('module_status', '')
            # print('Post data: = ', name, selected_team, description, submission_date, module_status)
            # print(Module.objects.filter(name__iexact=name),
            #       Module.objects.filter(name__iexact=name).exclude(name__iexact=selected_module.name), '000')

            date_obj = datetime.strptime(submission_date, '%Y-%m-%d')  # converting string date to date obj
            submission_date_obj = date_obj.date()  # datetime obj to save in model
            # print('Date:', submission_date_obj)
            today = datetime.today().date()
            # print(today)
            check_old_date = submission_date_obj - today  # checking whether given date is old than today
            # print(check_old_date)
            context = {'team_in_department': team_in_dep,
                       'name': name,
                       'description': description,
                       'selected_team': int(selected_team),
                       'submission_date': submission_date_obj.strftime("%Y-%m-%d"),
                       'selected_project': selected_project,
                       'module_status': module_status}
            # Validating the information
            module_update_error_link = 'departments/module_update.html'
            if check_old_date.days < 0:
                messages.warning(request, 'Please select a valid submission date.')
                return render(request, module_update_error_link, context)

            elif name.strip() == "":
                messages.warning(request, 'Please provide a module name')
                return render(request, module_update_error_link, context)

            elif Module.objects.filter(name__iexact=name).exclude(name__iexact=selected_module.name).exists():
                messages.warning(request, 'There is another module with this name. Please change the name.')
                return render(request, module_update_error_link, context)

            elif description.strip() == "":
                messages.warning(request, 'Please provide detail description of the module.')
                return render(request, module_update_error_link, context)

            elif selected_team == '':
                messages.warning(request, f"Please select a team!")
                return render(request, module_update_error_link, context)

            elif submission_date == '':
                messages.warning(request, f"Please provide submission date!")
                return render(request, module_update_error_link, context)

            elif submission_date_obj > selected_project.delivery_date:
                messages.warning(request,
                                 f"Project delivery date is {selected_project.delivery_date}."
                                 f" But you set submission date {submission_date_obj}!")
                return render(request, module_update_error_link, context)

            else:
                try:
                    #  Updating data

                    selected_team_obj = Team.objects.get(id=int(selected_team))  # getting the team obj.
                    selected_module.name = name  # creating a new module
                    selected_module.description = description
                    # selected_module.assigned_team = selected_team_obj
                    selected_module.project = selected_project
                    selected_module.submission_date = submission_date_obj
                    # if module_status != '':  # '' means not selecting any status
                    #     selected_module.status = int(module_status)  # setting the module

                    """ Setting notification as module is assigned to a team leader """
                    # getting the team leader
                    module_previously_assigned_team_leader = User.objects.get(team_member=selected_module.assigned_team,
                                                                              role__name__exact=role_team_leader)

                    """ If module is assigned already to a team and then only change the team then notification count"""

                    if (module_status == '' or int(
                            module_status) == 1) and selected_team_obj != selected_module.assigned_team and selected_module.status == 2:
                        print('1')
                        # if selected_team_obj != selected_module.assigned_team and selected_module.status == 2:
                        module_previously_assigned_team_leader.notification_count += 1  # increase previous leader notification count to tell that module is removed from him
                        module_previously_assigned_team_leader.save()
                        # create new task history object with module removed from previous team leader
                        task_history = TaskHistory()
                        task_history.module = selected_module
                        task_history.description = (model_to_dict(selected_module))
                        task_history.user = module_previously_assigned_team_leader
                        task_history.status = 'Module Removed'
                        task_history.save()

                        if module_status == '' or int(module_status) == 1:
                            selected_module.status = 1  # then change the status of the project to new
                            selected_module.assigned_at = None  # setting NOne as the status is new or not assigned
                            selected_module.save()

                        # if only change team with empty status
                        # if module_status == '' and selected_module.assigned_team != selected_team_obj:

                        """If module is assigned already to a leader and then change both the leader and 
                       status to assigned at same time"""
                    elif module_status != '' and selected_team_obj != selected_module.assigned_team and int(
                            module_status) == 2:
                        print('2')
                        # if selected_team_obj != selected_module.assigned_team and int(module_status) == 2:
                        # print('enter into same time change')
                        if selected_module in Module.objects.filter(assigned_team=selected_module.assigned_team, status=2):
                            module_previously_assigned_team_leader.notification_count += 1  # increase previous leader notification count to tell that module is removed from him
                            module_previously_assigned_team_leader.save()

                            task_history = TaskHistory()
                            task_history.module = selected_module
                            task_history.description = (model_to_dict(selected_module))
                            task_history.user = module_previously_assigned_team_leader  # this module is removed from this user
                            task_history.status = 'Module Removed'
                            task_history.save()

                        # adding the module to the new leader
                        selected_module.assigned_team = selected_team_obj
                        selected_module.save()
                        # print('updated team of the module is ::', selected_module.assigned_team, selected_module.assigned_team.get_team_leader())
                        new_leader_with_assigned_module_same_time = selected_module.assigned_team.team_member_user.get(
                            role__name__iexact=role_team_leader)
                        # print(new_leader_with_assigned_module_same_time, 'leader after team change with assign status')
                        new_leader_with_assigned_module_same_time.notification_count += 1
                        new_leader_with_assigned_module_same_time.save()
                        selected_module.status = 2
                        selected_module.assigned_at = datetime.now()
                        selected_module.team_leader_notified = False
                        selected_module.save()

                        task_history = TaskHistory()
                        task_history.module = selected_module
                        task_history.description = (model_to_dict(selected_module))
                        task_history.user = new_leader_with_assigned_module_same_time  # this module is added to this user
                        task_history.status = 'New Module'
                        task_history.save()

                        """ Assign module  to leader in edit mode then notification count..."""
                    elif module_status != '' and selected_module.status != 2 and int(module_status) == 2:  # if status is assigned
                        print('3')
                        # if selected project previous status not 2 means not assigned and user select 2 then...
                        # print('here selected module.status is not 2 and user select 2 so count++')
                        module_previously_assigned_team_leader.notification_count += 1  # Previously means at the time of creation of the module, the leadr who is selected.
                        module_previously_assigned_team_leader.save()
                        selected_module.assigned_at = datetime.now()  # setting the assigned date
                        selected_module.team_leader_notified = False
                        selected_module.save()
                        # create new task history object  for see the notification and history of tasks..
                        task_history = TaskHistory()
                        task_history.module = selected_module
                        task_history.description = (model_to_dict(selected_module))
                        task_history.user = module_previously_assigned_team_leader
                        task_history.status = 'New Module'
                        task_history.save()
                        print('module history created.====== module assigned to ',
                              module_previously_assigned_team_leader)
                        print(selected_module.status, 'selected module status....', module_status)

                        """ if module is already assigned then just changing the status of module."""
                    elif (module_status == '' or int(module_status) == 1) and selected_module.status == 2:  # if status is new or not assigned
                        print('4')
                        # if module previous status is 2 and user select 1 then only do --
                        print('here selected module.status is 2 and user select 1 so  count--')
                        module_previously_assigned_team_leader.notification_count += 1  # increase previous leader notification count to tell that module is removed from him
                        module_previously_assigned_team_leader.save()
                        selected_module.assigned_at = None  # setting NOne as the status is new or not assigned
                        selected_module.save()
                        # create new task history object
                        task_history = TaskHistory()
                        task_history.module = selected_module
                        task_history.description = (model_to_dict(selected_module))
                        task_history.user = module_previously_assigned_team_leader
                        task_history.status = 'Module Removed'
                        task_history.save()

                        # if module_assigned_team_leader.notification_count < 0:  # if notification count is < than 0
                        #     module_assigned_team_leader.notification_count = 0  # then make it 0
                        #     module_assigned_team_leader.save()
                    # setting status here because of notification count. if set up then got wrong notification. count value
                    # setting status here because of notification count.
                    # if set up then got wrong notification count value cause we checked db value of previous status
                    # which is updated by doing following thing.
                    if module_status != '':  # '' means not selecting any status
                        print('5')
                        selected_module.status = int(module_status)  # setting the module
                    selected_module.assigned_team = selected_team_obj
                    selected_module.save()  # saving module
                    messages.success(request, f"Module '{name}' is updated successfully!")
                    return redirect('department-project-details', project_code=selected_project.code)

                except Exception as e:
                    print("Error in module update: ", e)
                    messages.error(request, e)
                    return render(request, 'departments/module_update.html', context)


        return render(request, 'departments/module_update.html', context)


@login_required(login_url='login')
@has_access(allowed_roles=[role_department_head])
def module_delete(request, project_code, module_id):
    if request.user.is_authenticated:
        selected_project = get_object_or_404(Project, code=project_code)
        selected_module = get_object_or_404(Module, id=module_id)

        try:
            selected_module.delete()
            """ Setting notification count number as module is deleted """
            # getting the team leader
            module_assigned_team_leader = User.objects.get(team_member=selected_module.assigned_team,
                                                           role__name__exact=role_team_leader)
            # setting the notification count number as module is deleted
            if selected_module.status == 2:
                module_assigned_team_leader.notification_count -= 1
                module_assigned_team_leader.save()
            messages.success(request, f"Module '{selected_module.name}' is deleted!")
            return redirect('department-project-details', project_code=selected_project.code)

        except selected_project.DoesNotExist:
            messages.error(request, 'Module does not exist')
            return redirect('department-project-details', project_code=selected_project.code)

        except Exception as e:
            messages.error(request, f"Error: {e}.")
            return redirect('department-project-details', project_code=selected_project.code)


@login_required(login_url='login')
@has_access(allowed_roles=[role_department_head])
def module_assign(request, project_code, module_id):
    """
    After clicking on the assign module this function will run
    it will change the status of the module new to assigned
    """
    if request.user.is_authenticated:

        selected_project = get_object_or_404(Project, code=project_code)
        selected_module = get_object_or_404(Module, id=module_id)
        context = {'selected_project': selected_project,
                   'selected_module': selected_module}
        try:
            selected_module.status = 2  # status == 2 means module is assigned
            selected_module.assigned_at = datetime.now()  # setting the assigned date
            selected_module.team_leader_notified = False
            selected_module.save()

            # getting the team leader
            module_assigned_team_leader = User.objects.get(team_member=selected_module.assigned_team,
                                                           role__name__exact=role_team_leader)

            # create new task history object  for see the notification and history of tasks..
            task_history = TaskHistory()
            task_history.module = selected_module
            task_history.description = (model_to_dict(selected_module))
            task_history.status = 'New Module'
            task_history.user = module_assigned_team_leader
            task_history.save()
            print('module history created.====== module assigned to ', module_assigned_team_leader)

            """ Setting notification count number as module is assigned to a team leader """
            # # getting the team leader
            # module_assigned_team_leader = User.objects.get(team_member=selected_module.assigned_team,
            #                                                role__name__exact=role_team_leader)
            # print(module_assigned_team_leader)
            # setting the notification count number as project is assigned to team leader
            module_assigned_team_leader.notification_count += 1
            module_assigned_team_leader.save()

            messages.success(request,
                             f"{selected_module.name} is assigned to the {selected_module.assigned_team.name}.")
            return redirect('department-project-details', project_code=selected_project.code)
        except Exception as e:
            print('module assign error ====', e)
            messages.error(request, f"Error: {e}")
            return render(request, 'departments/department_project_details.html', context)
