from django.urls import path

from . import views

urlpatterns = [
    path('list/', views.department_list, name="department-list"),
    path('add/', views.department_add, name="department-add"),
    path('update/<str:department_name>/', views.department_update, name="department-update"),
    path('delete/<str:department_name>/', views.department_delete, name="department-delete"),

    path('project/all/', views.department_all_project, name="department-all-project"),
    path('project/<str:project_code>/', views.department_project_details, name="department-project-details"),
    path('project/completed', views.department_completed_project, name="department-completed-project"),
    path('project/running', views.department_running_project, name="department-running-project"),

    path('project/<str:project_code>/module/add/', views.module_create, name='module-create'),
    path('project/<str:project_code>/module/update/<int:module_id>', views.module_update,
         name='module-update'),
    path('project/<str:project_code>/module/delete/<int:module_id>/', views.module_delete,
         name='module-delete'),
    path('project/<str:project_code>/module/assign/<int:module_id>', views.module_assign,
         name="module-assign"),

]
