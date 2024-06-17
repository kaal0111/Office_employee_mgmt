from django.contrib import admin
from .models import Employee, Role, Department,Leave, Attendance,Salary
# Register your models here.

admin.site.register(Employee)
admin.site.register(Department)
admin.site.register(Role)
admin.site.register(Leave)
admin.site.register(Attendance)
admin.site.register(Salary)
