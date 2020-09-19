from accounts.models import User
from adminusers.models import Project, Module, Task, SubmittedToQATask


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

            """ all user role"""
            is_super_user_or_admin = request.user.role.name == 'Admin' or request.user.role.name == 'Super User'
            is_department_head = request.user.role.name == 'Department Head'
            is_team_leader = request.user.role.name == 'Team Leader'
            is_team_member = request.user.role.name == 'Team Member'
            is_employee = request.user.role.name == 'Employee'
            is_tester = request.user.role.name == 'Tester'
            """ NOTIFICATIONS SETTING """
            user_notification_count = User.objects.get(id=request.user.id).notification_count
            user_notification_item = None  # default notification item None
            """HEAD NOTIFICATION ITEM"""
            if is_department_head:
                # """ LIST OF NOTIFICATION ITEMS """
                user_notification_item = Project.objects.filter(department_id=request.user.department.id,
                                                                status=2).order_by('status', '-assigned_at')
                print('user_notification_item: -- ', user_notification_item, 'user notification count',
                      user_notification_count)
                if user_notification_count == 0:
                    user_notification_item = None
                    print('user_notification_item: -- ', user_notification_item, 'user notification count',
                          user_notification_count)

                return {'user_notification_count': user_notification_count,
                        'user_notification_item': user_notification_item,
                        'is_super_user_or_admin': is_super_user_or_admin,
                        'is_department_head': is_department_head,
                        'is_team_leader': is_team_leader,
                        'is_employee': is_employee,
                        'is_team_member': is_team_member,
                        'is_tester': is_tester}

            """Leader NOTIFICATION ITEM"""
            if request.user.team_member.id != 10 and is_team_leader:
                user_notification_item = Module.objects.filter(assigned_team=request.user.team_member,
                                                               status=2).order_by('status', '-assigned_at')
                print('user_notification_item: -- ', user_notification_item, 'user notification count',
                      user_notification_count)
                if user_notification_count == 0:
                    user_notification_item = None
                    print(user_notification_item, 'user notification count',
                          user_notification_count)
                return {'user_notification_count': user_notification_count,
                        'user_notification_item': user_notification_item,
                        'is_super_user_or_admin': is_super_user_or_admin,
                        'is_department_head': is_department_head,
                        'is_team_leader': is_team_leader,
                        'is_employee': is_employee,
                        'is_team_member': is_team_member,
                        'is_tester': is_tester }

            if is_team_member:
                user_notification_item = Task.objects.filter(assigned_member=request.user, status=2).order_by(
                    'status', '-assigned_at')
                print('user_notification_item: -- ', user_notification_item, 'user notification count',
                      user_notification_count)
                if user_notification_count == 0:
                    user_notification_item = None
                    print('user_notification_item: -- ', user_notification_item, 'user notification count',
                          user_notification_count)
                return {'user_notification_count': user_notification_count,
                        'user_notification_item': user_notification_item,
                        'is_super_user_or_admin': is_super_user_or_admin,
                        'is_department_head': is_department_head,
                        'is_team_leader': is_team_leader,
                        'is_employee': is_employee,
                        'is_team_member': is_team_member,
                        'is_tester': is_tester}

            if is_tester:
                user_notification_item = SubmittedToQATask.objects.filter(tester=request.user, status=3).order_by(
                    '-submitted_at')
                print('user_notification_item: -- ', user_notification_item, 'user notification count====',
                      user_notification_count)
                if user_notification_count == 0:
                    user_notification_item = None
                    print('user_notification_item: -- ', user_notification_item, 'user notification count',
                          user_notification_count)
                return {'user_notification_count': user_notification_count,
                        'user_notification_item': user_notification_item,
                        'is_super_user_or_admin': is_super_user_or_admin,
                        'is_department_head': is_department_head,
                        'is_team_leader': is_team_leader,
                        'is_employee': is_employee,
                        'is_team_member': is_team_member,
                        'is_tester': is_tester}
        return ''

    return ''  # return nothing
