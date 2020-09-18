from django.urls import path, include
from . import views
from .views import  login_view, logout_view, registration_view, forgot_password_view, security_code_view, change_password_view

urlpatterns = [
    path('', views.dashboard, name="dashboard"),
    path('login', login_view, name='login'),
    path('logout', logout_view, name='logout'),
    path('registration', registration_view, name='registration'),
    path('forgot', forgot_password_view, name='forgot_pass'),
    path('confirmation', security_code_view, name='security_code'),
    path('change_password', change_password_view, name='change_password'),
]


