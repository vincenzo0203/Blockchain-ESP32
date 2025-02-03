from django.urls import path
from . import views

urlpatterns = [
    path('check_uid/', views.check_uid, name='check_uid'),
    path('get_logs/', views.get_logs, name='get_logs'),
    path('get_login_admin/', views.get_admin_login_logs, name='get_login_admin'),
    path('get_action_admin/', views.get_admin_action_logs_view, name='get_action_admin'),
]
