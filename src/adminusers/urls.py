from django.urls import path
from . import views


urlpatterns = [
    path('dashboard', views.dashboard, name="admin-dashboard"),
    path('client-add', views.client_add, name="client-add"),
    path('client-list', views.client_list, name="client-list"),
    path('project-add', views.project_add, name="project-add"),
    path('project-list', views.project_list, name="project-list"),
    path('employee-list', views.employee_list, name="employee-list"),
    path('employee-add', views.employee_add, name="employee-add"),

]
