# core/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Department, Manager, Team, Employee
from .forms import DepartmentForm, DepartmentUpdateForm, ManagerForm, SignupForm, TeamForm, EmployeeForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User

def is_admin(user):
    return user.is_staff or user.is_superuser

# Dashboard - home page: list active departments & counts
@login_required
def dashboard(request):
    total_departments = Department.objects.count()
    active_departments = Department.objects.filter(status=True).count()
    total_managers = Manager.objects.count()
    active_managers = Manager.objects.filter(is_active=True).count()  
    total_employees = Employee.objects.count()
    active_employees = Employee.objects.filter(is_active=True).count()
    total_teams = Team.objects.count()
    active_teams = Team.objects.filter(status=True).count()

    context = {
        'total_departments': total_departments,
        'active_departments': active_departments,
        'total_managers': total_managers,
        'active_managers': active_managers,   
        'total_employees': total_employees,
        'active_employees': active_employees,
        'total_teams': total_teams,
        'active_teams': active_teams,
    }
    return render(request, 'core/dashboard.html', context)


# List departments (dashboard page can also link here)
@login_required
def department_list(request):
    q = request.GET.get('q', '')
    if q:
        departments = Department.objects.filter(dept_name__icontains=q)
    else:
        departments = Department.objects.all()
    return render(request, 'core/department_list.html', {'departments': departments, 'q': q})

# Create Department - Admin only
@login_required
@user_passes_test(is_admin)
def department_create(request):
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            dept = form.save(commit=False)
            dept.status = True
            dept.save()
            messages.success(request, f"Department '{dept.dept_name}' created successfully.")
            return redirect('core:department_list')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = DepartmentForm()
    return render(request, 'core/department_form.html', {'form': form, 'title': 'Add Department'})

# Update Department - Admin only
@login_required
@user_passes_test(is_admin)
def department_update(request, pk):
    dept = get_object_or_404(Department, pk=pk)
    if request.method == 'POST':
        form = DepartmentUpdateForm(request.POST, instance=dept)
        if form.is_valid():
            form.save()
            messages.success(request, f"Department '{dept.dept_name}' updated successfully.")
            return redirect('core:department_list')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = DepartmentUpdateForm(instance=dept)
    return render(request, 'core/department_form.html', {'form': form, 'title': 'Edit Department'})

# Soft delete (make inactive) - Admin only
@login_required
@user_passes_test(is_admin)
def department_delete(request, pk):
    dept = get_object_or_404(Department, pk=pk)
    # warn administrator that there may be related employees/managers
    if request.method == 'POST':
        # Set status to False (inactive)
        dept.status = False
        dept.save()
        messages.warning(request, f"Department '{dept.dept_name}' was marked inactive (soft deleted). Remember to reassign employees/managers.")
        return redirect('core:department_list')
    # GET: render a confirmation page
    return render(request, 'core/confirm_delete.html', {'object': dept, 'type': 'department'})

# Create Manager
@login_required
@user_passes_test(is_admin)
def manager_create(request):
    if request.method == 'POST':
        form = ManagerForm(request.POST)
        if form.is_valid():
            m = form.save()
            messages.success(request, f"Manager '{m.name}' created and assigned to '{m.department}'.")
            return redirect('core:department_list')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ManagerForm()
    return render(request, 'core/manager_form.html', {'form': form, 'title': 'Add Manager'})

def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            try:
                user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email, password=password)
                user.save()
                messages.success(request, "Registration successful! You can now log in.")
                return redirect('login')  # Redirect to login page after successful signup
            except Exception as e:
                messages.error(request, f"Error: {str(e)}")
        else:
            messages.error(request, "Passwords do not match.")

    return render(request, 'core/signup.html')

# Add Team
@login_required
@user_passes_test(is_admin)
def team_create(request):
    if request.method == 'POST':
        form = TeamForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Team created successfully.")
            return redirect('core:dashboard')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = TeamForm()
    return render(request, 'core/team_form.html', {'form': form, 'title': 'Add Team'})

# Add Employee
@login_required
@user_passes_test(is_admin)
def employee_create(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Employee added successfully.")
            return redirect('core:dashboard')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = EmployeeForm()
    return render(request, 'core/employee_form.html', {'form': form, 'title': 'Add Employee'})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('dashboard')  # Redirect to a dashboard or home page
        else:
            messages.error(request, "Invalid username or password.")
    
    return render(request, 'core/login.html')
