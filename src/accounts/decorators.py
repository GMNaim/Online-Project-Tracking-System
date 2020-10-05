from django.http import HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from django.urls import reverse


def has_access(allowed_roles=[]):
    def decorator(view_function):
        def wrap(request, *args, **kwargs):
            request.user.role.name = str(request.user.groups.all()[0])
            if request.user.role.name in allowed_roles:
                return view_function(request, *args, **kwargs)
            else:
                return HttpResponseRedirect(reverse('dashboard'))
        return wrap
    return decorator


def has_access_dashboard(allowed_roles=[]):
    def decorator(view_function):
        def wrap(request, *args, **kwargs):
            request.user.role.name = str(request.user.groups.all()[0])
            if request.user.role.name in allowed_roles:
                return view_function(request, *args, **kwargs)
            else:
                return HttpResponseRedirect(reverse('logout'))
        return wrap
    return decorator
