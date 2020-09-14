from django.contrib.auth.models import Group
from accounts.models import User


def left_sidebar_content(request):
    if request.user.is_authenticated:

        sidebar_department_name = None
        if request.user.department.id != 16:
            print('---------- id not `16')
            sidebar_department_name = request.user.department.name
        return {'sidebar_role_name': request.user.role.name, 'sidebar_department_name': sidebar_department_name}
    return ''  # return nothing
