from django.urls import path
from . import views


""" IF YOU CHANGE URL MUST CHANGE IN LIST PAGES"""
urlpatterns = [
    # path('list', views.team_list, name="team-list"),
    # path('add', views.team_add, name="team-add"),
    # path('update/<str:team_name>', views.team_update, name="team-update"),
    # # if you change url then must change in team_list.html.
    # path('delete/<str:team_name>', views.team_delete, name="team-delete"),


    path('task/all/', views.member_all_task, name="member-all-task"),
    path('task/<int:task_id>/', views.member_task_details, name="member-task-details"),
    path('task/test-passed/', views.member_test_passed_tasks, name="member-test-passed-task"),
    path('task/completed/', views.member_completed_tasks, name="member-completed-task"),
    path('task/running/', views.member_running_tasks, name="member-running-task"),
    path('task/submitted/', views.member_submitted_tasks, name="member-submitted-task"),
    path('task/submit_to_tester/<int:task_id>', views.submit_task_to_tester, name="submit-task"),
    path('task/need-modification/', views.member_need_modification_tasks, name="member-need-modification-task"),
    # path('task/send-leader/<int:task_id>', views.member_task_send_to_leader, name="member-task-send-leader"),

    # """ --------------      TESTER        ========================"""
    path('tester/task/all/', views.tester_all_task, name="tester-all-task"),
    path('tester/task/<int:task_id>/', views.tester_task_details, name="tester-task-details"),
    path('tester/task/completed/', views.tester_completed_tasks, name="tester-completed-task"),
    path('tester/task/running/', views.tester_running_tasks, name="tester-running-task"),
    # path('tester/task/submitted/', views.tester_submitted_tasks, name="tester-submitted-task"),

    # # TASK URLS
    # path('module/<int:module_id>/module/add/', views.task_create, name='task-create'),
    # path('module/<int:module_id>/task/update/<int:task_id>/', views.task_update,
    #      name='task-update'),
    # path('module/<int:module_id>/task/delete/<int:task_id>/', views.task_delete,
    #      name='task-delete'),
    # path('module/<int:module_id>/task/assign/<int:task_id>', views.task_assign,
    #      name="task-assign"),

]
