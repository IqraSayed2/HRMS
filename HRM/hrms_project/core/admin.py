# core/admin.py
from django.contrib import admin
from .models import Department, Manager, Team, Employee

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('dept_id','dept_name','status','created_at','updated_at')
    list_filter = ('status',)
    search_fields = ('dept_name',)

@admin.register(Manager)
class ManagerAdmin(admin.ModelAdmin):
    list_display = ('name','email','department','created_at')
    search_fields = ('name','email')

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name','department','status','created_at')
    list_filter = ('status',)
    search_fields = ('name','department__dept_name')

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('name','email','department','team','is_active','created_at')
    list_filter = ('is_active','department')
    search_fields = ('name','email')