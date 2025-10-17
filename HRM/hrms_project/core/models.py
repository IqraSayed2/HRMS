# core/models.py
from django.db import models
from django.utils import timezone

class Department(models.Model):
    dept_id = models.AutoField(primary_key=True)
    dept_name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=300, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)  # True = active, False = inactive (soft delete)

    def __str__(self):
        return self.dept_name

class Manager(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, related_name='managers')
    created_at = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True) 
    
    def __str__(self):
        return f"{self.name} ({self.email})"


class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=300, blank=True)
    manager = models.ForeignKey(Manager, on_delete=models.SET_NULL, null=True, blank=True, related_name='teams')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='teams')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)  # True=active, False=inactive

    def __str__(self):
        return self.name
    

class Employee(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, related_name='employees')
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True, related_name='employees')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name