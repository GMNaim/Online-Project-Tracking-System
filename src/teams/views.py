from django.shortcuts import render

# Create your views here.
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from .models import Team, Membership
from accounts.decorators import has_access

@login_required
def team_list(request):
    team = Team.objects.all()


    # for d in department:
    #     print(d.get_department_info())
    #     print(d.name, d.get_total_employee(), 'total employee----')

    # context = {'department': department, 'not_assigned': 'Not Assigned'}
    return render(request, 'teams/team_list.html')


@login_required
@has_access(allowed_roles=['Department Head'])
def team_add(request):
    if request.user.is_authenticated:
        team = Team.objects.all()
        membership = Membership.objects.all()
        context = {'team': team, 'membership': membership}
        if request.method == "POST":
            name = request.POST.get('name')
            team_member = request.POST.getlist('team_member')
            team_leader = request.POST.get('team_leader')
            description = request.POST.get('description')
            print(name, team_member, team_leader, description)

            # Validating the information
            team_add_error_link = 'teams/team_add.html'
            if name.strip() == "":
                context['team_member'] = team_member
                context['team_leader'] = team_leader
                context['description'] = description
                messages.warning(request, 'You must have to provide a team name')
                return render(request, team_add_error_link, context)

            elif Team.objects.filter(name=name).exists():
                context['team_member'] = team_member
                context['team_leader'] = team_leader
                context['description'] = description
                messages.warning(request, f"Team name {name} is already exists!")
                return render(request, team_add_error_link, context)



        return render(request, 'teams/team_add.html')


@login_required
def team_update(request, team_id):
    if request.user.is_authenticated:
        return render(request, 'teams/team_update.html')


@login_required
def team_delete(request, team_id):
    if request.user.is_authenticated:
        return render(request, 'teams/team_list.html')
