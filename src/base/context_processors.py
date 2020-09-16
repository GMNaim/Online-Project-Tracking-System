from accounts.models import User
from adminusers.models import Project


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
            head_notification_count = User.objects.get(department_id=request.user.department.id,
                                                       role__name__iexact='Department Head').notification_count  # all projects that are assigned to the head
            """ LIST OF NOTIFICATION ITEMS """
            assigned_projects_to_head = Project.objects.filter(department_id=request.user.department.id,
                                                               status=2).order_by('status', '-modified_at')

            return {'head_notification_count': head_notification_count,
                    'assigned_projects_to_head': assigned_projects_to_head}

    return ''  # return nothing
