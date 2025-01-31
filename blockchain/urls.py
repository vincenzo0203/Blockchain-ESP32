from django.urls import path
from . import views

urlpatterns = [
    path('check_uid/', views.check_uid, name='check_uid'),
    path('get_logs/', views.get_logs, name='get_logs'),
]
