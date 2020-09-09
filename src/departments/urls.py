from django.urls import path
from . import views


urlpatterns = [
    path('list', views.department_list, name="department-list"),
    path('add', views.department_add, name="department-add"),
    path('update/<str:department_name>', views.department_update, name="department-update"),
    path('delete/<str:department_name>', views.department_delete, name="department-delete"),

]
