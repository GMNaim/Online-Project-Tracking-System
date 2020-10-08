from django.db.models import Q

from accounts.models import User
from projectmanager.models import TaskHistory



role_super_user = 'Super User'
role_pm = 'Project Manager'
role_department_head = 'Department Head'
role_team_leader = 'Team Leader'
role_team_member = 'Team Member'
role_employee = 'Employee'
role_tester = 'Tester'


def left_sidebar_content(request):
    if request.user.is_authenticated:

        """ all user role"""
        is_super_user_or_pm = request.user.role.name == role_pm or request.user.role.name == role_super_user
        is_department_head = request.user.role.name == role_department_head
        is_team_leader = request.user.role.name == role_team_leader
        is_team_member = request.user.role.name == role_team_member
        is_employee = request.user.role.name == role_employee
        is_tester = request.user.role.name == role_tester

        sidebar_department_name = None
        if request.user.department.id != 16:
            sidebar_department_name = request.user.department.name
        return {'sidebar_role_name': request.user.role.name,
                'sidebar_department_name': sidebar_department_name,
                'is_super_user_or_pm': is_super_user_or_pm,
                'is_department_head': is_department_head,
                'is_team_leader': is_team_leader,
                'is_employee': is_employee,
                'is_team_member': is_team_member,
                'is_tester': is_tester}
    return ''  # return nothing


def nav_bar_content(request):
    if request.user.is_authenticated:
        if request.user.department.id != 16:

            """ all user role"""
            is_super_user_or_pm = request.user.role.name == role_pm or request.user.role.name == role_super_user
            is_department_head = request.user.role.name == role_department_head
            is_team_leader = request.user.role.name == role_team_leader
            is_team_member = request.user.role.name == role_team_member
            is_employee = request.user.role.name == role_employee
            is_tester = request.user.role.name == role_tester
            """ NOTIFICATIONS SETTING """
            user_notification_count = User.objects.get(id=request.user.id).notification_count
            user_notification_item = None  # default notification item None
            """HEAD NOTIFICATION ITEM"""
            if is_department_head:
                """ LIST OF NOTIFICATION ITEMS """
                # user_notification_item = Project.objects.filter(department_id=request.user.department.id,
                #                                                 status=2).order_by('status', '-assigned_at')
                user_notification_item = TaskHistory.objects.filter(user=request.user).order_by('-created_at')[:10]
                print('user_notification_item: -- ', user_notification_item, 'user notification count',
                      user_notification_count)
                # if user_notification_count == 0:
                #     user_notification_item = None
                #     print('user_notification_item: -- ', user_notification_item, 'user notification count',
                #           user_notification_count)

                return {'user_notification_count': user_notification_count,
                        'user_notification_item': user_notification_item,
                        'is_super_user_or_pm': is_super_user_or_pm,
                        'is_department_head': is_department_head,
                        'is_team_leader': is_team_leader,
                        'is_employee': is_employee,
                        'is_team_member': is_team_member,
                        'is_tester': is_tester}

            """Leader NOTIFICATION ITEM"""
            if request.user.team_member.id != 10 and is_team_leader:
                # user_notification_item = TaskHistory.objects.filter(Q(module__assigned_team=request.user.team_member,
                #                                                       module__status__in=[1, 2]) | Q(
                #     module__assigned_team=request.user.team_member,
                #     task__status=7)).order_by('-created_at')[:user_notification_count]
                # user_notification_item = TaskHistory.objects.filter(Q(module__assigned_team=request.user.team_member,
                #                                                       module__status__in=[1, 2]) | Q(
                #     module__assigned_team=request.user.team_member, task__status=7)).order_by('-created_at')[:9]
                user_notification_item = TaskHistory.objects.filter(user=request.user).order_by('-created_at')[:10]

                print('leader user_notification_item: -- ', user_notification_item, 'user notification count',
                      user_notification_count)
                # if user_notification_count == 0:
                #     user_notification_item = None

                return {'user_notification_count': user_notification_count,
                        'user_notification_item': user_notification_item,
                        'is_super_user_or_pm': is_super_user_or_pm,
                        'is_department_head': is_department_head,
                        'is_team_leader': is_team_leader,
                        'is_employee': is_employee,
                        'is_team_member': is_team_member,
                        'is_tester': is_tester}

            """member NOTIFICATION ITEM"""
            if is_team_member:
                # user_notification_item = Task.objects.filter(assigned_member=request.user, status__in=[2, 5, 6]).order_by(
                #     'status', '-assigned_at')
                # user_notification_item = TaskHistory.objects.filter(task__assigned_member=request.user,
                #                                                     task__status__in=[2, 5, 6]).order_by(
                #     '-created_at')[:user_notification_count]

                user_notification_item = TaskHistory.objects.filter(user=request.user).order_by('-created_at')[:10]

                print('user_notification_item: -- ', user_notification_item, 'user notification count',
                      user_notification_count)

                # if user_notification_count == 0:
                #     user_notification_item = None
                #     print('user_notification_item: -- ', user_notification_item, 'user notification count',
                #           user_notification_count)
                return {'user_notification_count': user_notification_count,
                        'user_notification_item': user_notification_item,
                        'is_super_user_or_pm': is_super_user_or_pm,
                        'is_department_head': is_department_head,
                        'is_team_leader': is_team_leader,
                        'is_employee': is_employee,
                        'is_team_member': is_team_member,
                        'is_tester': is_tester}

            """tester NOTIFICATION ITEM"""
            if is_tester:
                # user_notification_item = SubmittedToQATask.objects.filter(tester=request.user, status=3).order_by(
                #     '-submitted_at')
                # user_notification_item = TaskHistory.objects.filter(
                #     submitted_task__assigned_member=request.user, submitted_task__task__status=4).order_by(
                #     '-created_at')[:user_notification_count]
                user_notification_item = TaskHistory.objects.filter(user=request.user).order_by('-created_at')[:10]

                print('user_notification_item: -- ', user_notification_item, 'user notification count=',
                      user_notification_count)
                # if user_notification_count == 0:
                #     user_notification_item = None
                #     print('user_notification_item: -- ', user_notification_item, 'user notification count',
                #           user_notification_count)
                return {'user_notification_count': user_notification_count,
                        'user_notification_item': user_notification_item,
                        'is_super_user_or_pm': is_super_user_or_pm,
                        'is_department_head': is_department_head,
                        'is_team_leader': is_team_leader,
                        'is_employee': is_employee,
                        'is_team_member': is_team_member,
                        'is_tester': is_tester}
        return ''

    return ''  # return nothing
