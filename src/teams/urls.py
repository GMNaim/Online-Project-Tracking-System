from django.urls import path
from . import views


urlpatterns = [
    path('team/list', views.team_list, name="team-list"),
    path('team/add', views.team_add, name="team-add"),
    path('team/update/<str:team_name>', views.team_update, name="team-update"),
    # if you change url then must change in team_list.html.
    path('team/delete/<str:team_name>', views.team_delete, name="team-delete"),


    path('team/module/all/', views.team_all_module, name="team-all-module"),
    path('team/module/<int:module_id>/', views.team_module_details, name="team-module-details"),
    path('team/module/completed/', views.team_completed_modules, name="team-completed-module"),
    path('team/module/running/', views.team_running_modules, name="team-running-module"),
    # TASK URLS
    path('team/module/<int:module_id>/module/add/', views.task_create, name='task-create'),
    path('team/module/<int:module_id>/task/update/<int:task_id>/', views.task_update,
         name='task-update'),
    path('team/module/<int:module_id>/task/delete/<int:task_id>/', views.task_delete,
         name='task-delete'),
    path('team/module/<int:module_id>/task/assign/<int:task_id>', views.task_assign,
         name="task-assign"),

]
