from django.urls import path
from . import views


urlpatterns = [
    path('department/list/', views.department_list, name="department-list"),
    path('department/add/', views.department_add, name="department-add"),
    path('department/update/<str:department_name>/', views.department_update, name="department-update"),
    path('department/delete/<str:department_name>/', views.department_delete, name="department-delete"),


]
