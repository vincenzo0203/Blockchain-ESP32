# backend/accounts/urls.py
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('user_management/', views.user_management_view, name='user_management'),
    path('user_access/', views.user_access_view, name='user_access'),
    path('person/add/', views.person_add, name='person_add'),
    path('person/edit/', views.person_edit, name='person_edit'),
    path('person/delete/', views.person_delete, name='person_delete'),
]
