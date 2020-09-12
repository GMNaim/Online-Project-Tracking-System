# Create your views here.
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
from accounts.decorators import has_access
from accounts.models import User, Role
from departments.models import Department
from .models import Team, Membership


@login_required
def team_list(request):
    team = Team.objects.all()

    # for d in department:
    #     print(d.get_department_info())
    #     print(d.name, d.get_total_employee(), 'total employee----')

    # context = {'department': department, 'not_assigned': 'Not Assigned'}
    return render(request, 'teams/team_list.html')


@login_required
@has_access(allowed_roles=['Department Head', 'Admin'])  # for testing admin is getting parmission
def team_add(request):
    if request.user.is_authenticated:
        department_name = Department.objects.get(name__iexact=request.user.department.name)

        membership = Membership.objects.all()
        print(request.user.department.name)
        free_employee_in_department = User.objects.filter(department__name=request.user.department.name).exclude(
            role__name__iexact='Department Head').filter(membership__is_member=False)
        print(free_employee_in_department, '------- employee in the department without head')
        context = {'employee_in_department': free_employee_in_department}
        # print(free_employee_in_department)
        # for e in free_employee_in_department:
        #     print(e.username, e.role, 'employee--')
        # print(all_member_list, all_member_list.count())
        if request.method == "POST":
            team_name = request.POST.get('name')
            team_member = request.POST.getlist('team_member')
            team_leader = request.POST.get('team_leader')
            description = request.POST.get('description')
            print(team_name, team_member, team_leader, description, type(team_member))

            # Validating the information
            team_add_error_link = 'teams/team_add.html'
            if team_name.strip() == "":
                context['team_member'] = team_member
                context['team_leader'] = team_leader
                context['description'] = description
                messages.warning(request, 'You must have to provide a team team_name')
                return render(request, team_add_error_link, context)

            elif Team.objects.filter(name=team_name).exists():
                context['team_member'] = team_member
                context['team_leader'] = team_leader
                context['description'] = description
                messages.warning(request, f"Team team_name {team_name} is already exists!")
                return render(request, team_add_error_link, context)

            else:
                try:
                    team = Team.objects.create(name=team_name, department=department_name)
                    # team.team_name = team_name
                    # team.department = department_name
                    # team.members.set(team_member)
                    # team.save()
                    print(f" Team {team} saved in the database.")
                    #  removing the member from team_member if he is also a team leader
                    if team_leader in team_member:
                        team_member.remove(team_leader)
                    print(team_member)

                    # getting leader id
                    membership_leader = membership.get(user_id=team_leader)
                    print(membership_leader.user.id)
                    # setting the leader for the team
                    for free_employee in free_employee_in_department:
                        if free_employee.id == membership_leader.user.id:
                            membership_leader.team = Team.objects.get(name__iexact=str(team_name))
                            membership_leader.is_leader = True
                            membership_leader.is_member = True
                            membership_leader.save()
                            # setting the role to the employee
                            user_leader = User.objects.get(id=team_leader)  # getting the user
                            user_leader.role = Role.objects.get(name__iexact='Team Leader')  # setting the role
                            user_leader.save()  # saving
                            print(f"{user_leader.username}: {user_leader.id} -->", user_leader.role.name)
                            # Adding Team Leader to team leader group.
                            group = Group.objects.get(name__iexact='Team Leader')
                            print('Group name:=> ', group)
                            group.user_set.add(user_leader)
                            group = Group.objects.get(name__iexact='Team Member')
                            group.user_set.add(user_leader)

                    # Adding team Members
                    for member in team_member:
                        membership_member = Membership.objects.get(user_id=member)  # getting individual team member
                        print(membership_member.user.username, '---> ', membership_member.user.id)
                        membership_member.team = Team.objects.get(name__iexact=str(team_name))  # updating the team name
                        membership_member.is_member = True  # updating is_member
                        membership_member.save()
                        # setting the role to the employee
                        user_member = User.objects.get(id=member)  # getting the user
                        user_member.role = Role.objects.get(name__iexact='Team Member')  # setting the role
                        user_member.save()
                        print(user_member.username, '-->', user_member.id,'==>', user_member.role.name)

                        # Adding Team member to team member group.
                        group = Group.objects.get(name__iexact='Team Member')
                        print('Group name:=> ', group)
                        group.user_set.add(user_member)

                    messages.success(request, f"Team {team_name} is successfully created.")
                    return redirect('team-list')

                except Exception as e:
                    print("Error:------", e)
                    messages.ERROR(request, f"Error: {e}")
                    return render(request, 'teams/team_add.html', context)

        return render(request, 'teams/team_add.html', context)


@login_required
def team_update(request, team_id):
    if request.user.is_authenticated:
        return render(request, 'teams/team_update.html')


@login_required
def team_delete(request, team_id):
    if request.user.is_authenticated:
        return render(request, 'teams/team_list.html')
