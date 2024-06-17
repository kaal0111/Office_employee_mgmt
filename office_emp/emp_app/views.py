from datetime import datetime
from urllib import request
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from .models import Employee, Role, Department,Leave, Attendance, Salary

# Create your views here.
def index(request):
    return render(request, 'index.html' )

def view_all(request):
    emps = Employee.objects.all()
    context = {
        'emps': emps
        }
    print(context)
    return render(request, 'view_all.html', context)

def add_emp(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        dept = int(request.POST['dept'])
        role = int(request.POST['role'])
        phone = int(request.POST['phone'])
        email = request.POST['email']
        # hire_date = request.POST['hire_date']
        new_emp = Employee(first_name=first_name, last_name=last_name,dept_id=dept, role_id=role,phone=phone,email=email,hire_date=datetime.now().date())
        new_emp.save()
        return HttpResponse('Employee added Successfully!')
        
    elif request.method == 'GET':  
        return render(request, 'add_emp.html' )
    else:
        return HttpResponse('An Exception Occured! Employee Has Not Been Added!!')
    

def leave(request):
    leaves = Leave.objects.all().order_by('-start_date')
    return render(request, 'leave.html', {"leaves":leaves})

def leave_status(request, leave_id):
    if request.method == 'POST':
        leave = get_object_or_404(Leave, id=leave_id)
        new_status = request.POST.get('status')
        if new_status in ['approved','rejected']:
            leave_status = new_status
            leave.save()
    return redirect('leave_approved')



def mark_attendance(request):
    attends = Attendance.objects.all()
    return render(request, 'mark_attendance.html', {'attends':attends})