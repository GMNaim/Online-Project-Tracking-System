from django.urls import path, include
from . import views

""" IF YOU CHANGE URL MUST CHANGE IN LIST PAGES"""
urlpatterns = [
    path('client/add', views.client_add, name="client-add"),
    path('client/list', views.client_list, name="client-list"),
    path('client/update/<str:client_id>', views.client_update, name="client-update"),
    path('client/delete/<str:client_id>', views.client_delete, name="client-delete"),

    path('project/add', views.project_add, name="project-add"),
    path('project/update/<str:project_code>', views.project_update, name="project-update"),
    path('project/delete/<str:project_code>', views.project_delete, name="project-delete"),
    path('project/list', views.project_list, name="project-list"),
    path('project/assign/<str:project_code>', views.project_assign, name="project-assign"),
    path('project/completed/', views.pm_completed_projects, name="project-completed"),

    path('employee/list', views.employee_list, name="employee-list"),
    path('employee/add', views.employee_add, name="employee-add"),
    path('employee/update/<str:employee_username>', views.employee_update, name="employee-update"),
    path('employee/delete/<str:employee_username>', views.employee_delete, name="employee-delete"),
    # path('department/', include('departments.urls')),



]
