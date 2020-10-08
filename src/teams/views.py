# teams/views.py


# Create your views here.
from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.forms import model_to_dict
from django.shortcuts import render, redirect, get_object_or_404

from accounts.decorators import has_access
from accounts.models import User, Role
from departments.models import Department
from projectmanager.models import Module, Task, TaskHistory
from teams.models import Team

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
@has_access(allowed_roles=[role_pm, role_department_head, role_super_user])
def team_list(request):
    if request.user.is_authenticated:

        """ ======================       work with new model data  ============================="""
        all_team = Team.objects.exclude(id=10)
        # for t in all_team:
        #     print(t.get_total_member(), '------------------------------------- &&&&&&&&&&&&&& ', t.name)
        #     print(t.get_team_leader(), '------------------------------------- &&&&&&&&&&&&&& ', t.name)
        """ Team in all department """
        all_team_leader = []
        all_team_members = []
        all_member_count = []
        all_team_name = []
        all_team_dep = []
        if all_team.count() != 0:
            for team in all_team:
                print(f"team Name: {team}")
                all_team_name.append(team.name)
                print(all_member_count.append(team.team_member_user.count()))
                all_team_dep.append(team.department)
                team_l = team.team_member_user.get(is_team_leader=True)
                all_team_leader.append(team_l)
                all_team_members.append(', '.join(list(team.team_member_user.values_list('username', flat=True))))
        all_team_zipped = zip(all_team_name, all_team_leader, all_team_members, all_member_count, all_team_dep)

        """ team in department """
        team_in_dep = all_team.filter(department__name__iexact=request.user.department.name).exclude(
            department_id=16)  # department id = 16 is the Not Assigned dep.
        print(team_in_dep.count() == 0)
        team_leader = []
        team_members = []
        member_count = []
        team_name = []
        team_dep = []
        if team_in_dep.count() != 0:
            for team in team_in_dep:
                print(f"team Name: {team}")
                team_name.append(team.name)
                print(member_count.append(team.team_member_user.count()))
                team_dep.append(team.department)
                team_l = team.team_member_user.get(is_team_leader=True)
                team_leader.append(team_l)
                team_members.append(', '.join(list(team.team_member_user.values_list('username', flat=True))))

        team_zipped = zip(team_name, team_leader, team_members, member_count, team_dep)
        context = {"team_in_dep": team_in_dep, 'team_zipped': team_zipped, 'all_team_zipped': all_team_zipped}

        return render(request, 'teams/team_list.html', context)


@login_required(login_url='login')
@has_access(
    allowed_roles=[role_department_head, role_pm, role_super_user])  # for testing role_pm is getting permission
def team_add(request):
    if request.user.is_authenticated:
        # requested users department
        department = Department.objects.get(name__iexact=request.user.department.name)
        free_employee_in_department = User.objects.filter(department=department, is_tester=False).exclude(
            role__name__exact=role_department_head).filter(team_member_id=10)
        # for free_employee in free_employee_in_department:
        #     print(free_employee.username)
        # print(free_employee_in_department, free_employee_in_department.count(), '************************')
        context = {'free_employee_in_department': free_employee_in_department}
        if request.method == "POST":
            team_name = str(request.POST.get('name')).strip()
            team_member = request.POST.getlist('team_member')
            team_leader = request.POST.get('team_leader')
            description = request.POST.get('description')
            print(team_name, team_member, team_leader, description, type(team_member))

            # Validating the information
            team_add_error_link = 'teams/team_add.html'
            context['team_member'] = team_member
            context['team_leader'] = team_leader
            context['description'] = description

            if team_name.strip() == "":
                messages.warning(request, 'You must have to provide a team name')
                return render(request, team_add_error_link, context)

            elif Team.objects.filter(name=team_name).exists():
                messages.warning(request, f"Team team_name {team_name} is already exists!")
                return render(request, team_add_error_link, context)

            elif team_leader not in team_member:
                messages.warning(request,
                                 f"You have selected "
                                 f"{free_employee_in_department.get(id=team_leader).username} "
                                 f"as team leader but he is not team member!")
                return render(request, team_add_error_link, context)

            elif len(team_member) == 0:
                messages.warning(request, f"You have to select at least one team member!")
                return render(request, team_add_error_link, context)

            elif team_leader == "":
                messages.warning(request, f"You must have to select a team leader")
                return render(request, team_add_error_link, context)

            else:
                try:
                    """ SAVING ALL DATA RELATED TO TEAM """

                    # if you create a team  you must have to select a team leader.
                    team = Team.objects.create(name=team_name, department=department)  # team created
                    print(f" Team {team} saved in the database.")
                    new_team_members = free_employee_in_department.filter(pk__in=team_member)
                    new_team_leader_object = free_employee_in_department.filter(id=team_leader)
                    print('team members', new_team_members)
                    new_team_leader = new_team_leader_object.first()  # as it is the first obj of queryset
                    print(new_team_leader, "team leader")

                    """ Adding the team leader to the new team and setting role and permission group"""
                    new_team_leader.team_member = team  # adding the team for the user
                    # setting the role to the employee
                    new_team_leader.role = Role.objects.get(name__iexact=role_team_leader)  # setting the role
                    new_team_leader.is_team_leader = True
                    new_team_leader.save()
                    print(f"{new_team_leader.username}: {new_team_leader.id} -->", new_team_leader.role.name)
                    # Adding Team Leader to team leader group and team member group.
                    group_team_leader.user_set.add(new_team_leader)
                    group_team_member.user_set.add(new_team_leader)
                    group_employee.user_set.add(new_team_leader)

                    """ Adding the team members to the new team and setting role and permission group"""
                    for new_member in new_team_members:
                        new_member.team_member = Team.objects.get(
                            name__iexact=str(team_name))  # adding the team for the user
                        new_member.role = Role.objects.get(name__iexact=role_team_member)  # setting the role
                        new_member.save()
                        # Adding Team member to team member group.
                        group_team_member.user_set.add(new_member)
                        group_employee.user_set.add(new_member)

                    messages.success(request, f"Team {team_name} is successfully created.")
                    return redirect('team-list')

                except Exception as e:
                    messages.success(request, f"Error: {e}")
                    print('Error: ', e)
                    return redirect('team-add')

    return render(request, 'teams/team_add.html', context)


@login_required(login_url='login')
@has_access(allowed_roles=[role_department_head, role_pm, role_super_user])
def team_update(request, team_name):
    if request.user.is_authenticated:
        # get the team
        team = get_object_or_404(Team, name=team_name)
        print(team.name)
        team_members = User.objects.filter(team_member=team)
        existing_team_member_list = []
        existing_team_leader = ''
        # Getting the team members and team leader
        for mem in team_members:
            existing_team_member_list.append(mem)
            print(mem.username, mem.is_team_leader, '3333')
            if mem.is_team_leader:
                existing_team_leader = mem

        print(existing_team_member_list, existing_team_leader)
        print(type(existing_team_leader), type(existing_team_member_list), existing_team_member_list)
        # requested users department
        department = Department.objects.get(name__iexact=request.user.department.name)
        free_employee_in_department_and_team_members = User.objects.filter(department=department).exclude(
            role__name__exact=role_department_head).filter(
            team_member_id__in=[10, team.id])  # Getting free and selected team's members

        context = {'free_employee_in_department': free_employee_in_department_and_team_members,
                   'team_member_list': existing_team_member_list,
                   'team_leader': existing_team_leader, 'team_name': team.name}
        # Getting user post data
        if request.method == "POST":
            team_name = str(request.POST.get('name')).strip()
            team_member = request.POST.getlist('team_member')
            team_leader = request.POST.get('team_leader')
            description = request.POST.get('description')
            print(team_member, '0000000000000000000000000')
            print(team_name, team_member, team_leader, description, type(team_member))
            context.update({'description': description})
            # Validating the information
            team_update_error_link = 'teams/team_update.html'

            if team_name.strip() == "":
                messages.warning(request, 'You must have to provide a team name')
                return render(request, team_update_error_link, context)

            elif Team.objects.filter(name=team_name).exclude(name__iexact=team_name).exists():
                messages.warning(request, f"Team team_name {team_name} is already exists!")
                return render(request, team_update_error_link, context)

            elif team_leader not in team_member:
                messages.warning(request,
                                 f"You have selected "
                                 f"{free_employee_in_department_and_team_members.get(id=team_leader).username} "
                                 f"as team leader but he is not team member!")
                return render(request, team_update_error_link, context)

            elif len(team_member) == 0:
                messages.warning(request, f"Please select team members")
                return render(request, team_update_error_link, context)

            elif team_leader == "":
                messages.warning(request, f"You must have to select a team leader")
                return render(request, team_update_error_link, context)

            else:
                try:
                    """ SAVING UPDATED DATA RELATED TO TEAM """

                    team.name = team_name  # updating team name
                    team.description = description
                    team.save()
                    """ Getting new team members and new team leader """
                    new_team_members = []
                    for member in free_employee_in_department_and_team_members.filter(pk__in=team_member):
                        new_team_members.append(member)
                    print('new team members*********', new_team_members, type(new_team_members))
                    new_team_leader = free_employee_in_department_and_team_members.get(id=team_leader)
                    print(new_team_leader, "team leader")
                    print('-------------------------------------------------------------')

                    """ Adding the team leader to the new team and setting role and permission group"""

                    # checking whether new team leader is the existing one or not
                    if new_team_leader.username != existing_team_leader.username:
                        new_team_leader.team_member = team  # adding the member to the team.
                        # setting the role to the employee
                        new_team_leader.role = Role.objects.get(name__iexact=role_team_leader)  # setting the role
                        new_team_leader.is_team_leader = True
                        new_team_leader.save()

                        """ Changing the attributes of old team leader."""
                        existing_team_leader.role = Role.objects.get(
                            name__iexact=role_team_member)  # giving old team leader to employee role
                        existing_team_leader.is_team_leader = False  # as he is not a leader now so false.
                        existing_team_leader.save()  # saving update of existing team leader.

                        print(f"{new_team_leader.username}: {new_team_leader.id} -->",
                              new_team_leader.role.name,
                              f"Existing team leader status: {existing_team_leader.team_member.name},"
                              f" {existing_team_leader.is_team_leader}, {existing_team_leader.role.name}")
                        # Adding Team Leader to team leader and team member group.
                        group_team_leader.user_set.add(new_team_leader)
                        group_team_member.user_set.add(new_team_leader)
                        group_employee.user_set.add(new_team_leader)
                        # changing the existing team leader group
                        existing_team_leader.groups.remove(group_team_leader)  # removing the group from old team leader

                    """ Adding the team members to the new team and setting role and permission group"""
                    common_member_in_new_and_existing = set(existing_team_member_list) & set(new_team_members)
                    # print(common_member_in_new_and_existing, '----------------')
                    removed_member_from_existing = list(
                        set(existing_team_member_list) - set(common_member_in_new_and_existing))
                    only_new_member = list(set(new_team_members) - set(common_member_in_new_and_existing))

                    # Setting team properties to the new members
                    if len(only_new_member) != 0:
                        for member in only_new_member:
                            member.team_member = team  # adding the team for the member
                            member.role = Role.objects.get(name__iexact='Team Member')  # setting the role
                            member.save()
                            # Adding Team member to team member group.
                            group_team_member.user_set.add(member)
                            group_employee.user_set.add(member)

                    # changing removed member's status
                    if len(removed_member_from_existing) != 0:
                        for member in removed_member_from_existing:
                            member.team_member = Team.objects.get(id=10)  # setting default team.
                            member.role = Role.objects.get(name__iexact='Employee')  # setting the role
                            member.save()
                            # removing Team member group and setting employee group
                            member.groups.remove(group_team_member)
                            group_employee.user_set.add(member)

                    messages.success(request, f"Team {team_name} is successfully updated.")
                    return redirect('team-list')

                except Exception as e:
                    messages.error(request, f"Error: {e}")
                    print('Error: ', e)
                    return render(request, 'teams/team_update.html', context)

        return render(request, 'teams/team_update.html', context)


@login_required(login_url='login')
@has_access(allowed_roles=[role_pm, role_super_user, role_department_head])
def team_delete(request, team_name):
    if request.user.is_authenticated:
        # get the team
        team = get_object_or_404(Team, name=team_name)

        print(team.name, team.department, team)
        team_members = User.objects.filter(team_member=team)
        selected_teams_member_list = []
        selected_teams_leader = ''
        # Getting the team members and team leader
        for mem in team_members:
            selected_teams_member_list.append(mem)
            if mem.is_team_leader:
                selected_teams_leader = mem

        print(selected_teams_member_list, selected_teams_leader)
        print(type(selected_teams_leader), type(selected_teams_member_list), selected_teams_member_list)
        # requested users department
        department = Department.objects.get(name__iexact=request.user.department.name)
        free_employee_in_department_and_team_members = User.objects.filter(department=department).exclude(
            role__name__exact="Department Head").filter(
            team_member_id__in=[10, team.id])  # Getting free and selected team's members

        context = {'free_employee_in_department': free_employee_in_department_and_team_members,
                   'team_member_list': selected_teams_member_list,
                   'team_leader': selected_teams_leader, 'team_name': team.name}
        try:
            team.delete()
            """ Changing the attributes of deleted team leader and members."""
            selected_teams_leader.team_member = Team.objects.get(id=10)  # setting default team.
            selected_teams_leader.role = Role.objects.get(
                name__iexact=role_employee)  # giving deleted team's leader to role_employee role
            selected_teams_leader.is_team_leader = False  # as he is not a leader now so false.
            selected_teams_leader.save()  # saving update of deleted team leader.
            # changing the existing team leader group
            selected_teams_leader.groups.remove(group_team_leader)  # removing the group from deleted team leader
            selected_teams_leader.groups.remove(group_team_member)  # removing the group from deleted team leader
            group_employee.user_set.add(selected_teams_leader)  # setting employee permission group

            # changing deleted team's member status
            if len(selected_teams_member_list) != 0:
                for member in selected_teams_member_list:
                    member.team_member = Team.objects.get(id=10)  # setting default team.
                    member.role = Role.objects.get(name__iexact=role_employee)  # setting the role
                    member.save()
                    # removing Team member group and setting employee group
                    member.groups.remove(group_team_member)

            print(f"{team} deleted..............")
            messages.success(request, f"Team '{team.name}' is deleted!")
            return redirect('team-list')
        except team.DoesNotExist:
            messages.error(request, 'Team does not exist')
            return redirect('team-list')
        except Exception as e:
            messages.error(request, f"Error: {e}.")
            return render(request, 'teams/team_list.html', context)


def team_member_list(request):
    if request.user.is_authenticated:
        members = User.objects.filter(team_member=request.user.team_member)
        context = {'members': members, 'active': 'active'}
        for mem in members:
            print(mem.username, mem.team_member.name, 'task no', mem.task_set.count())
        return render(request, 'teams/team_member_list.html', context)


""" ==============================================  TASK WORK  =============================================="""


@login_required(login_url='login')
@has_access(allowed_roles=[role_team_leader])
def team_all_module(request):
    # user_notification_item = Module.objects.filter(
    #     assigned_team__team_member_user__username__iexact=request.user.username, status__gte=2)
    # print(user_notification_item, ' = user_notification_item')
    assigned_modules_list_to_leader = Module.objects.filter(assigned_team=request.user.team_member,
                                                            status__gte=2).order_by('-assigned_at', 'status')

    """ CHANGING THE NOTIFICATION COUNT TO ZERO as he see the notification """
    current_user = User.objects.get(id=request.user.id)
    current_user.notification_count = 0
    current_user.save()

    """ LIST OF NOTIFICATION ITEMS """
    # user_notification_item = Module.objects.filter(assigned_team=request.user.team_member, status=2).order_by(
    #      '-assigned_at', 'status')
    # print('user_notification_item: -- ', user_notification_item)
    # if current_user.notification_count == 0:
    #     user_notification_item = None

    context = {'assigned_modules_list_to_leader': assigned_modules_list_to_leader}
    return render(request, 'teams/team_all_module.html', context)


@login_required(login_url='login')
@has_access(allowed_roles=[role_team_leader])
def team_running_modules(request):
    if request.user.is_authenticated:
        running_modules = Module.objects.filter(status=3, assigned_team=request.user.team_member).order_by(
            '-assigned_at')  # 3 means running modules
        context = {'running_modules': running_modules}
        return render(request, 'teams/team_running_modules.html', context)


@login_required(login_url='login')
@has_access(allowed_roles=[role_team_leader])
def team_completed_modules(request):
    if request.user.is_authenticated:
        completed_modules = Module.objects.filter(status=4, assigned_team=request.user.team_member).order_by(
            '-assigned_at')  # 4 means completed modules
        context = {'completed_modules': completed_modules}
        return render(request, 'teams/team_completed_modules.html', context)


@login_required(login_url='login')
@has_access(allowed_roles=[role_team_leader])
def team_module_details(request, module_id):
    if request.user.is_authenticated:
        # user_notification_item = Project.objects.filter(department_id=request.user.department.id, status=2)
        selected_module = get_object_or_404(Module, id=module_id)
        selected_module.team_leader_notified = True  # as leader visit detail page so he is notified
        selected_module.save()
        print(selected_module.status, '---------------')
        task_list = Task.objects.filter(module_id=module_id)  # task list of the selected module
        print(task_list.count())

        """ CHANGING THE NOTIFICATION COUNT TO ZERO as he see the notification"""
        current_user = User.objects.get(id=request.user.id)
        current_user.notification_count = 0
        current_user.save()

        """ LIST OF NOTIFICATION ITEMS making zero as he see the notification... """
        # user_notification_item = Module.objects.filter(assigned_team=request.user.team_member, status=2).order_by(
        #     '-assigned_at', 'status')
        # print('user_notification_item: -- ', user_notification_item)
        # if current_user.notification_count == 0:
        #     user_notification_item = None

        #  If there is at least one task created then module status will be change to running.
        if selected_module.status != 4 and task_list.count() > 0:
            selected_module.status = 3  # if any task then status will be 3 means running
            selected_module.save()

        #
        # """ ============= Module completed ============="""
        # all_task = task_list.count()
        # task_complete_counter = 0
        # print(task_list, type(task_list), all_task)
        #
        # for task in task_list:
        #     print(task.get_status_display())
        #     if task.status == 7:
        #         task_complete_counter += 1  # if task is completed then increment then compare it with total task.
        #
        # if all_task == task_complete_counter:
        #     selected_module.status = 4
        #     selected_module.is_completed = True
        #     selected_module.completed_at = datetime.now()
        #     selected_module.save()
        # else:
        #     selected_module.is_completed = False
        #     selected_module.status = 3
        #     selected_module.completed_at = None
        #     selected_module.save()

        context = {'selected_module': selected_module,
                   'task_list': task_list}
        return render(request, 'teams/team_module_details.html', context)


@login_required(login_url='login')
@has_access(allowed_roles=[role_team_leader, role_super_user, role_pm])
def task_create(request, module_id):
    if request.user.is_authenticated:
        selected_module = get_object_or_404(Module, id=module_id)
        # members_in_team = Team.objects.filter(team_member_user__department_id=request.user.department.id).exclude(
        #     id=10).distinct()  # getting all team of signed in department head's department
        members_in_team = User.objects.filter(team_member__id=request.user.team_member.id)
        # print('member in the team ', members_in_team)

        context = {'selected_module': selected_module, 'members_in_team': members_in_team}

        if request.method == "POST":
            name = str(request.POST['name']).strip()
            selected_member = request.POST['selected_member']
            description = request.POST['description']
            submission_date = request.POST['submission_date']
            # print('Post data: = ', name, selected_member, description, submission_date)

            date_obj = datetime.strptime(submission_date, '%Y-%m-%d')  # converting string date to date obj
            submission_date_obj = date_obj.date()  # datetime obj to save in model
            # print('Date:', submission_date_obj)
            today = datetime.today().date()
            # print(today)
            check_old_date = submission_date_obj - today  # checking whether given date is old than today
            # print(check_old_date)
            context = {'members_in_team': members_in_team,
                       'name': name,
                       'description': description,
                       'selected_member': int(selected_member),
                       'submission_date': submission_date_obj.strftime("%Y-%m-%d"),
                       'selected_module': selected_module, }
            # Validating the information
            task_add_error_link = 'teams/task_add.html'
            if check_old_date.days < 0:
                messages.warning(request, 'Please select a valid submission date.')
                return render(request, task_add_error_link, context)

            elif name.strip() == "":
                messages.warning(request, 'Please provide task name')
                return render(request, task_add_error_link, context)
            #
            # elif Task.objects.filter(name__iexact=name).exists():
            #     messages.warning(request, 'There is another task with this name. Please change the name.')
            #     return render(request, task_add_error_link, context)

            elif description.strip() == "":
                messages.warning(request, 'Please provide detail description of the task.')
                return render(request, task_add_error_link, context)

            elif selected_member == '':
                messages.warning(request, f"Please select a member!")
                return render(request, task_add_error_link, context)

            elif submission_date == '':
                messages.warning(request, f"Please provide submission date!")
                return render(request, task_add_error_link, context)

            elif submission_date_obj > selected_module.submission_date:
                messages.warning(request,
                                 f"Module delivery date is {selected_module.submission_date}."
                                 f" But you set task submission date {submission_date_obj}!")
                return render(request, task_add_error_link, context)

            else:
                try:
                    #  Saving new task data to database

                    selected_member_obj = User.objects.get(id=int(selected_member))  # getting the member obj.
                    task = Task(name=name,  # creating a new task
                                description=description,
                                assigned_member=selected_member_obj,
                                module=selected_module,
                                submission_date=submission_date_obj)
                    task.save()  # saving new created task
                    print(task.module.name)
                    # #  If there is at least one module created then project status will be change to running.
                    # if selected_project.module_set.all().count() > 0:
                    #     selected_project.status = 3  # if any module then status will be 3 means nunning
                    #     selected_project.save()
                    messages.success(request, f"Task '{name}' is created successfully!")
                    return redirect('team-module-details', module_id=selected_module.id)
                except Exception as e:
                    print('Error at creating task: ', e)
                    messages.error(request, e)
                    return render(request, task_add_error_link, context)

        return render(request, 'teams/task_add.html', context)


@login_required(login_url='login')
@has_access(allowed_roles=[role_team_leader, role_super_user, role_pm])
def task_update(request, module_id, task_id):
    if request.user.is_authenticated:
        selected_module = get_object_or_404(Module, id=module_id)  # getting the selected module
        selected_task = get_object_or_404(Task, id=task_id)
        members_in_team = User.objects.filter(team_member__id=request.user.team_member.id)
        print('member in the team ', members_in_team)

        context = {'members_in_team': members_in_team,
                   'selected_module': selected_module,
                   'selected_task': selected_task,
                   'name': selected_task.name,
                   'description': selected_task.description,
                   'submission_date': selected_task.submission_date.strftime("%Y-%m-%d"),  # its converting date
                   'task_status': selected_task.status}

        if request.method == "POST":
            name = str(request.POST['name']).strip()
            selected_member = request.POST['selected_member']
            description = request.POST.get('description')
            submission_date = request.POST.get('submission_date')
            task_status = request.POST.get('task_status', '')
            # print('Post data: = ', name, selected_member, description, submission_date, task_status)

            date_obj = datetime.strptime(submission_date, '%Y-%m-%d')  # converting string date to date obj
            submission_date_obj = date_obj.date()  # datetime obj to save in model
            # print('Date:', submission_date_obj)
            today = datetime.today().date()
            # print(today)
            check_old_date = submission_date_obj - today  # checking whether given date is old than today
            # print(check_old_date)
            context = {'members_in_team': members_in_team,
                       'selected_module': selected_module,
                       'selected_task': selected_task,
                       'name': selected_task.name,
                       'description': selected_task.description,
                       'submission_date': selected_task.submission_date.strftime("%Y-%m-%d"),  # its converting date
                       'task_status': selected_task.status}
            # Validating the information
            task_update_error_link = 'teams/task_update.html'
            if check_old_date.days < 0:
                messages.warning(request, 'Please select a valid submission date.')
                return render(request, task_update_error_link, context)

            elif name.strip() == "":
                messages.warning(request, 'Please provide a task name.')
                return render(request, task_update_error_link, context)

            elif description.strip() == "":
                messages.warning(request, 'Please provide description of the task.')
                return render(request, task_update_error_link, context)

            elif selected_member == '':
                messages.warning(request, f"Please select a team member!")
                return render(request, task_update_error_link, context)

            elif submission_date == '':
                messages.warning(request, f"Please provide submission date!")
                return render(request, task_update_error_link, context)

            elif submission_date_obj > selected_module.submission_date:
                messages.warning(request,
                                 f"Module submission date is {selected_module.submission_date}."
                                 f" But you set task submission date {submission_date_obj}!")
                return render(request, task_update_error_link, context)

            else:
                try:
                    #  Updating task data
                    newly_selected_member_obj = User.objects.get(
                        id=int(selected_member))  # getting the team member obj.
                    # print('selected member for task ==', newly_selected_member_obj)
                    previously_assigned_member = selected_task.assigned_member

                    # creating a new task
                    selected_task.name = name
                    selected_task.description = description
                    # selected_task.assigned_member = selected_member_obj  # setting member below as if user set member after assigned another member
                    selected_task.module = selected_module
                    selected_task.submission_date = submission_date_obj

                    """ Setting notification as task is assigned to a team member """


                    """ If task is assigned already to a member and then just change the member
                     then notification count"""
                    if (task_status == '' or int(
                            task_status) == 1) and newly_selected_member_obj != previously_assigned_member and selected_task.status == 2:
                        print('1')
                        previously_assigned_member.notification_count += 1  # increase previous member notification count to tell that task is removed from
                        previously_assigned_member.save()
                        # create new task history object
                        task_history = TaskHistory()
                        task_history.task = selected_task
                        task_history.description = (model_to_dict(selected_task))
                        task_history.status = 'Task Removed'
                        task_history.user = previously_assigned_member
                        task_history.save()

                        if task_status == '' or int(task_status) == 1:
                            selected_task.status = 1  # then change the status of the
                            selected_task.assigned_at = None  # setting NOne as the status is new or not assigned
                            selected_task.save()


                        """If task is assigned already to a member and then change both the member and 
                       status to assigned-status at the same time """
                    elif task_status != '' and newly_selected_member_obj != previously_assigned_member and int(
                            task_status) == 2:
                        print('2 is printing')
                        # if newly_selected_member_obj != previously_assigned_member and int(task_status) == 2:
                        # print('enter into same time change')

                        if selected_task in Task.objects.filter(assigned_member=selected_task.assigned_member, status=2):
                            selected_task.assigned_member.notification_count += 1  # increase previous head notification count to tell that project is removed from
                            previously_assigned_member.save()

                            task_history = TaskHistory()
                            task_history.task = selected_task
                            task_history.description = (model_to_dict(selected_task))
                            task_history.status = 'Task Removed'
                            task_history.user = previously_assigned_member
                            task_history.save()

                        # adding the task to the new member
                        selected_task.assigned_member = newly_selected_member_obj
                        selected_task.save()

                        newly_selected_member_obj.notification_count += 1
                        newly_selected_member_obj.save()
                        selected_task.status = 2
                        selected_task.assigned_at = datetime.now()
                        selected_task.team_member_notified = False
                        selected_task.save()
                        # create new task history object
                        task_history = TaskHistory()
                        task_history.task = selected_task
                        task_history.description = (model_to_dict(selected_task))
                        task_history.status = 'New Task'
                        task_history.user = newly_selected_member_obj
                        task_history.save()

                        # print(selected_task.status, 'selected selected_task status....', task_status)
                        """ Assign task to member in edit mode then notification count..."""
                    elif task_status != '' and selected_task.status != 2 and int(task_status) == 2:  # if status is assigned
                        print('3')
                        # if selected project previous status not 2 means not assigned and user select 2 then...
                        # print('here selected module.status is not 2 and user select 2 so count++')
                        newly_selected_member_obj.notification_count += 1  # Then increase the notification count
                        newly_selected_member_obj.save()
                        selected_task.assigned_at = datetime.now()  # setting the assigned date
                        selected_task.team_member_notified = False
                        selected_task.save()
                        # create new task history object
                        task_history = TaskHistory()
                        task_history.task = selected_task
                        task_history.description = (model_to_dict(selected_task))
                        task_history.status = 'New Task'
                        task_history.user = newly_selected_member_obj
                        task_history.save()
                        # print('previously selected task status.', selected_task.status, 'task status:', task_status)

                        """ just change the status of the task from assigned to new """
                    elif (task_status == '' or int(task_status) == 1) and selected_task.status == 2:  # if status is new or not assigned
                        print('4')
                        # if module previous status is 2 and user select 1 then only do --
                        # print('here selected selected_task.status is 2 and user select 1 so  count--')
                        previously_assigned_member.notification_count += 1  # increase previous member notification count to tell that task is removed from him
                        previously_assigned_member.save()
                        selected_task.assigned_at = None  # setting NOne as the status is new or not assigned
                        selected_task.save()
                        # create new task history object
                        task_history = TaskHistory()
                        task_history.task = selected_task
                        task_history.description = (model_to_dict(selected_task))
                        task_history.status = 'Task Removed'
                        task_history.user = previously_assigned_member
                        task_history.save()

                    # setting status here because of notification count. if set up then got wrong notifica. count value
                    # setting status here because of notification count.
                    # if set up then got wrong notification count value cause we checked db value of previous status
                    # which is updated by doing following thing.
                    if task_status != '':  # '' means not selecting any status
                        print('5')
                        selected_task.status = int(task_status)  # setting the module
                    selected_task.assigned_member = newly_selected_member_obj
                    selected_task.save()  # saving module
                    messages.success(request, f"Task '{name}' is updated successfully!")
                    return redirect('team-module-details', module_id=selected_module.id)

                except Exception as e:
                    print("Error in task update: ", e)
                    messages.error(request, e)
                    return render(request, task_update_error_link, context)

        return render(request, 'teams/task_update.html', context)


@login_required(login_url='login')
@has_access(allowed_roles=[role_team_leader])
def task_delete(request, module_id, task_id):
    if request.user.is_authenticated:
        selected_module = get_object_or_404(Module, id=module_id)
        selected_task = get_object_or_404(Task, id=task_id)

        try:
            selected_task.delete()
            """ Setting notification count number as task is deleted """
            # getting the team member
            task_assigned_team_member = selected_task.assigned_member
            # setting the notification count number as module is deleted
            if selected_task.status == 2:
                task_assigned_team_member.notification_count -= 1
                task_assigned_team_member.save()
            messages.success(request, f"Task '{selected_task.name}' is deleted!")
            return redirect('team-module-details', module_id=selected_module.id)

        except selected_task.DoesNotExist:
            messages.error(request, 'Task does not exist')
            return redirect('team-module-details', module_id=selected_module.id)

        except Exception as e:
            messages.error(request, f"Error: {e}.")
            return redirect('team-module-details', module_id=selected_module.id)


@login_required(login_url='login')
@has_access(allowed_roles=[role_team_leader, role_super_user, role_pm])
def task_assign(request, module_id, task_id):
    """
    After clicking on the assign task button  this function will run
    it will change the status of the module new to assigned
    """
    if request.user.is_authenticated:
        selected_task = get_object_or_404(Task, id=task_id)
        selected_module = get_object_or_404(Module, id=module_id)
        context = {'selected_task': selected_task,
                   'selected_module': selected_module}
        try:
            """ Setting notification count number as task is assigned to a team member """
            # getting the team member
            task_assigned_team_member = selected_task.assigned_member

            selected_task.status = 2  # status == 2 means task is assigned
            selected_task.assigned_at = datetime.now()  # setting the assigned date
            selected_task.save()
            # create new task history object
            task_history = TaskHistory()
            task_history.task = selected_task
            task_history.description = (model_to_dict(selected_task))
            task_history.status = 'New Task'
            task_history.user = task_assigned_team_member
            task_history.save()

            # setting the notification count numger as task is assigned to team member
            task_assigned_team_member.notification_count += 1
            task_assigned_team_member.save()

            messages.success(request,
                             f"{selected_task.name} is assigned to the {selected_task.assigned_member}.")
            return redirect('team-module-details', module_id=selected_module.id)
        except Exception as e:
            print('task assign error ====', e)
            messages.error(request, f"Error: {e}")
            return render(request, 'teams/team_module_details.html', context)


"""==============================================   QA TEAM TASK   ==============================================="""
