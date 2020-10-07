from django.urls import path
from . import views


""" IF YOU CHANGE URL MUST CHANGE IN LIST PAGES"""
urlpatterns = [
    path('list', views.team_list, name="team-list"),
    path('add', views.team_add, name="team-add"),
    path('update/<str:team_name>', views.team_update, name="team-update"),
    # if you change url then must change in team_list.html.
    path('delete/<str:team_name>', views.team_delete, name="team-delete"),
    path('my-team-members/', views.team_member_list, name="my-team-members"),


    path('module/all/', views.team_all_module, name="team-all-module"),
    path('module/<int:module_id>/', views.team_module_details, name="team-module-details"),
    path('module/completed/', views.team_completed_modules, name="team-completed-module"),
    path('module/running/', views.team_running_modules, name="team-running-module"),
    # TASK URLS
    path('module/<int:module_id>/module/add/', views.task_create, name='task-create'),
    path('module/<int:module_id>/task/update/<int:task_id>/', views.task_update,
         name='task-update'),
    path('module/<int:module_id>/task/delete/<int:task_id>/', views.task_delete,
         name='task-delete'),
    path('module/<int:module_id>/task/assign/<int:task_id>', views.task_assign,
         name="task-assign"),

]
