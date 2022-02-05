from django.db import models
from datetime import time

class Department(models.Model):
    '''
    This model is used to define which
    Department an employee belongs too
    '''
    department = models.CharField('Department', max_length=256)

    def __str__(self):
        return self.department

class AttendanceConstraint(models.Model):
    '''
    Defines when can an Employee tick
    an attendance. For example it is only
    allowed to tick your attendance 
    from 2:00 AM to 2:30 AM.

    We are doing it like this because some
    employee have special permission to leave
    earlier than other employees

    mg_en_str: morning entry start
    mg_en_stp: morning entry stop

    mg_ex_str: morning exit start
    mg_ex_stp: morning exit stop

    an_en_str: afernoon entry start
    an_en_stp: afernoon entry stop

    an_ex_str: afernoon exit start
    an_ex_stp: afernoon exit stop

    mg_ex_stp_fr: friday morning exit stop
    '''
    constraint_name = models.CharField('Constraint Name', default="Normal", max_length=120)

    mg_en_str = models.TimeField('Morning Entry Start ⤵', default=time(7, 30))
    mg_en_stp = models.TimeField('Morning Entry Stop  ⤴', default=time(9))
    
    mg_ex_str = models.TimeField('Morning Exit Start ⤵', default=time(11, 45))
    mg_ex_stp = models.TimeField('Morning Exit Stop  ⤴', default=time(13, 30))

    an_en_str = models.TimeField('Afternoon Entry Start ⤵', default=time(14))
    an_en_stp = models.TimeField('Afternoon Entry Stop  ⤴', default=time(15))

    an_ex_str = models.TimeField('Afternoon Exit Start ⤵', default=time(16, 45))
    an_ex_stp = models.TimeField('Afternoon Exit Stop  ⤴', default=time(18, 0))

    mg_ex_str_fr = models.TimeField('Friday Morning Exit Start ⤵', default=time(10, 45))

    def __str__(self):
        return f"Constraint: {self.constraint_name}"

class Permission(models.Model):
    permission_start = models.DateField('Permission Start')
    permission_stop = models.DateField('Permission Stop')
    permission_name = models.CharField('Permission Name', max_length=256)
    letter_of_permission = models.FileField('Letter of permission')

    def __str__(self):
        return self.permission_name

class Employee(models.Model):
    '''
    Employee information like:
        - Full Name
        - Occupation
        - Sex
        - ID Number
        - Department
        - Attendance Constraint
    '''
    GENDER = (
        ('Male', 'Male'),
        ('Female', 'Female')
    )

    full_name = models.CharField('Full Name', max_length=70)
    occupation = models.CharField('Occupation', max_length=256)
    sex = models.CharField('Sex', choices=GENDER, max_length=10)
    id_number = models.CharField('ID Number', unique=True, max_length=50)
    image = models.ImageField(upload_to='photos')

    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    attendance_constraint = models.ForeignKey(AttendanceConstraint, 
                                              on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE, blank=True, null=True)

    salary = models.FloatField()

    def __str__(self):
        return self.full_name

    def show_desc(self):
        return self.occupation

class Attendance(models.Model):
    '''
    The attendance of each employee
    '''
    STATUS = (
        ('absent', 'Absent'),
        ('present', 'Present'),
        ('permission', 'Permission'),
    )
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField('Date', auto_now=True, )

    morning_entry = models.TimeField('Morning Entry', blank=True, null=True)
    morning_exit = models.TimeField('Morning Exit', blank=True, null=True)
    afternoon_entry = models.TimeField('Afternoon Entry', blank=True, null=True)
    afternoon_exit = models.TimeField('Afternoon Exit', blank=True, null=True)

    def __str__(self):
        return f"Attns for {self.employee}"


class PermissionHistory(models.Model):
    permission_start = models.DateField('Permission Start')
    permission_stop = models.DateField('Permission Stop')
    permission_name = models.CharField('Permission Name', max_length=256)
    letter_of_permission = models.FileField('Letter of permission')

    permission_owner = models.ForeignKey(Employee, on_delete=models.CASCADE)

    def __str__(self):
        return self.permission_name
