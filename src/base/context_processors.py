from accounts.models import User
from adminusers.models import Project, Module


def left_sidebar_content(request):
    if request.user.is_authenticated:

        sidebar_department_name = None
        if request.user.department.id != 16:
            sidebar_department_name = request.user.department.name
        return {'sidebar_role_name': request.user.role.name, 'sidebar_department_name': sidebar_department_name}
    return ''  # return nothing


def nav_bar_content(request):
    if request.user.is_authenticated:
        if request.user.department.id != 16:
            """ NOTIFICATIONS SETTING """
            """HEAD NOTIFICATION COUNT"""
            head_notification_count = User.objects.get(department_id=request.user.department.id,
                                                       role__name__iexact='Department Head').notification_count  # all projects that are assigned to the head
            """ LIST OF NOTIFICATION ITEMS """
            assigned_projects_to_head = Project.objects.filter(department_id=request.user.department.id,
                                                               status=2).order_by('status', '-modified_at')

            """ TEAM LEADER NOTIFICATION COUNT"""
            team_leader_notification_count = User.objects.get(id=request.user.id).notification_count
            print('Team leader notification count', team_leader_notification_count)

            """ LIST OF NOTIFICATION ITEMS """
            assigned_modules_to_leader = Module.objects.filter(assigned_team=request.user.team_member, status=2).order_by('status', '-modified_at')
            print('assigned_modules_to_leader: -- ', assigned_modules_to_leader)
            if team_leader_notification_count == 0:
                assigned_modules_to_leader = None
            return {'head_notification_count': head_notification_count,
                    'assigned_projects_to_head': assigned_projects_to_head,
                    'team_leader_notification_count': team_leader_notification_count,
                    'assigned_modules_to_leader': assigned_modules_to_leader}

    return ''  # return nothing
