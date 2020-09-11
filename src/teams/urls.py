from django.urls import path
from . import views


urlpatterns = [
    path('list', views.team_list, name="team-list"),
    path('add', views.team_add, name="team-add"),
    path('update/<int:team_id>', views.team_update, name="team-update"),
    path('delete/<int:team_id>', views.team_delete, name="team-delete"),

]
