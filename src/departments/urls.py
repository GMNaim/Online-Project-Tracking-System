from django.urls import path

from . import views

urlpatterns = [
    path('department/list/', views.department_list, name="department-list"),
    path('department/add/', views.department_add, name="department-add"),
    path('department/update/<str:department_name>/', views.department_update, name="department-update"),
    path('department/delete/<str:department_name>/', views.department_delete, name="department-delete"),

    path('department/project/all/', views.department_all_project, name="department-all-project"),
    path('department/project/<str:project_code>/', views.department_project_details, name="department-project-details"),
    path('department/project/completed/', views.department_completed_project, name="department-completed-project"),
    path('department/project/running/', views.department_running_project, name="department-running-project"),

    path('department/project/<str:project_code>/module/add/', views.module_create, name='module-create'),
    path('department/project/<str:project_code>/module/update/<int:module_id>/', views.module_update,
         name='module-update'),
    path('department/project/<str:project_code>/module/delete/<int:module_id>/', views.module_delete,
         name='module-delete'),
    path('department/project/<str:project_code>/module/assign/<int:module_id>', views.module_assign,
         name="module-assign"),

]
