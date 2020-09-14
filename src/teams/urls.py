from django.urls import path
from . import views


urlpatterns = [
    path('team/list', views.team_list, name="team-list"),
    path('team/add', views.team_add, name="team-add"),
    path('team/update/<str:team_name>', views.team_update, name="team-update"),
    # if you change url then must change in team_list.html.
    path('team/delete/<str:team_name>', views.team_delete, name="team-delete"),

]
