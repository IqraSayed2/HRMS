# core/urls.py
from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('departments/', views.department_list, name='department_list'),
    path('departments/add/', views.department_create, name='department_create'),
    path('departments/<int:pk>/edit/', views.department_update, name='department_update'),
    path('departments/<int:pk>/delete/', views.department_delete, name='department_delete'),
    path('managers/add/', views.manager_create, name='manager_create'),
    path('teams/add/', views.team_create, name='team_create'),
    path('employees/add/', views.employee_create, name='employee_create'),
]
