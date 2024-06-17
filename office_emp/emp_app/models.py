from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

# Model for department
class Department(models.Model):
    name =  models.CharField(max_length=100, null=False)
    location = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

# Model for Roles  
class Role(models.Model):
    name = models.CharField(max_length=100,null=False)
    
    def __str__(self):
        return self.name
    
# Model for Employee
class Employee(models.Model):
    first_name = models.CharField(max_length=100, null=False)
    last_name = models.CharField(max_length=100)
    dept = models.ForeignKey(Department, on_delete=models.CASCADE)
    # salary = models.OneToOneField(Salary,on_delete=models.CASCADE)
    # bonus = models.IntegerField(default=0)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    phone = models.IntegerField(default=0)
    email = models.EmailField(null=True)
    hire_date = models.DateField()
    
    def __str__(self):
        return "%s %s %s" %(self.first_name, self.last_name, self.phone)
    
    days_present = models.FloatField(default=0)

    def update_days_present(self):
        total_days = self.attendance_records.aggregate(
            total=sum('days_present')
        )['total'] or 0
        self.days_present = total_days
        self.save()
    
# Model for Leave

class Leave(models.Model):
    emp = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='leaves')
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=(
        ('pending', 'Pending'),
        ('approved','Approved'),
        ('rejected', 'Rejected')
    ),default='pending')
    num_days = models.PositiveBigIntegerField(validators=[MinValueValidator(1), MaxValueValidator(30)])
    
    def __str__(self):
        return f"{self.emp.first_name} {self.emp.last_name} - {self.start_date} to {self.end_date}"
    
# Model for Attendance
class Attendance(models.Model):
    emp = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='attendance_records')
    date = models.DateField()
    status = models.CharField(max_length=10, choices=(
        ('not marked', 'Not Marked'),
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('half day', 'Half Day'),
        ('leave', 'Leave'),
    ), default='Not Marked')
    remarks = models.TextField(blank=True, null=True)
    days_present = models.FloatField(default=0)

    def save(self, *args, **kwargs):
        if self.status == 'present':
            self.days_present = 1
        elif self.status == 'half day':
            self.days_present = 0.5
        else:
            self.days_present = 0
        super().save(*args, **kwargs)
        self.emp.update_days_present()

    
# Model for Salary
class Salary(models.Model):
    emp = models.OneToOneField(Employee, on_delete=models.CASCADE, related_name='salary')
    base_salary = models.DecimalField(max_digits=10, decimal_places=2)
    benefits = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    bonus = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    deductions = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    @property
    def net_salary(self):
        return self.base_salary + self.benefits + self.bonus - self.deductions
    
    def __str__(self):
        return f"{self.emp.first_name} {self.emp.last_name} - Salary"
    