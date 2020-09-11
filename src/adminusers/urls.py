from django.urls import path, include
from . import views


urlpatterns = [
    path('client/add', views.client_add, name="client-add"),
    path('client/list', views.client_list, name="client-list"),
    path('project/add', views.project_add, name="project-add"),
    path('project/list', views.project_list, name="project-list"),
    path('employee/list', views.employee_list, name="employee-list"),
    path('employee/add', views.employee_add, name="employee-add"),
    path('employee/update/<str:employee_username>', views.employee_update, name="employee-update"),
    path('employee/delete/<str:employee_username>', views.employee_delete, name="employee-delete"),
    path('department/', include('departments.urls')),
    path('team/', include('teams.urls')),


]
