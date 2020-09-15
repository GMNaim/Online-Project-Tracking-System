# teams/views.py


# Create your views here.
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect, get_object_or_404

from accounts.decorators import has_access
from accounts.models import User, Role
from departments.models import Department
from teams.models import Team

# Role Names
role_super_user = 'Super User'
role_admin = 'Admin'
role_department_head = 'Department Head'
role_team_leader = 'Team Leader'
role_team_member = 'Team Member'
role_employee = 'Employee'

default_password = 'test123'  # default pass
# getting user group
group_super_user = Group.objects.get(name__iexact=role_super_user)
group_admin = Group.objects.get(name__iexact=role_admin)
group_department_head = Group.objects.get(name__iexact=role_department_head)
group_team_leader = Group.objects.get(name__iexact=role_team_leader)
group_team_member = Group.objects.get(name__iexact=role_team_member)
group_employee = Group.objects.get(name__iexact=role_employee)


@login_required
@has_access(allowed_roles=[role_admin, role_department_head, role_super_user])
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


@login_required
@has_access(
    allowed_roles=[role_department_head, role_admin, role_super_user])  # for testing role_admin is getting permission
def team_add(request):
    if request.user.is_authenticated:
        # requested users department
        department = Department.objects.get(name__iexact=request.user.department.name)
        free_employee_in_department = User.objects.filter(department=department).exclude(
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


@login_required
@has_access(allowed_roles=[role_department_head, role_admin, role_super_user])
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


@login_required
@has_access(allowed_roles=[role_admin, role_super_user, role_department_head])
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
