from django.contrib import admin
from django.contrib.auth.models import Group
from django.db import models
from django.forms import NumberInput

from .models import AttendanceConstraint, Department, Employee, Attendance, Permission, PermissionHistory

@admin.register(Employee)
class EmployeeDefined(admin.ModelAdmin):
    list_display = ('full_name', 'occupation', 'department', 'sex', 'id_number',
                    'attendance_constraint', 'permission')
    list_filter = ('occupation', 'sex', 'department')
    search_fields = ('full_name', 'occupation', 'id_number')
    formfield_overrides = {
        models.IntegerField: {'widget': NumberInput(attrs={'size': '20'})}
    }

@admin.register(Attendance)
class AttendanceDefined(admin.ModelAdmin):
    list_filter = ('date', 'employee',)
    search_fields = ('employee__full_name', 'date')
    readonly_fields = ( 
        'employee',
        'morning_entry', 'morning_exit',
        'afternoon_entry', 'afternoon_exit',
    )
    list_display = (
        'employee', 'date', 'morning_entry', 'morning_exit',
        'afternoon_entry', 'afternoon_exit',
    )

@admin.register(AttendanceConstraint)
class AttendanceConstraintDefined(admin.ModelAdmin):
    list_filter = ('constraint_name',)
    search_fields = ('constraint_name',)
    list_display = (
        'constraint_name',

        'mg_en_str',
        'mg_en_stp',

        'mg_ex_str',
        'mg_ex_stp',

        'an_en_str',
        'an_en_stp',

        'an_ex_str',
        'an_ex_stp',
    )

@admin.register(Department)
class DepartmentDefined(admin.ModelAdmin):
    list_display = ('department',)
    search_fields = ('department',)
    list_filter = ('department',)

@admin.register(Permission)
class PermissionDefined(admin.ModelAdmin):
    list_display = ('permission_name', 'permission_start', 'permission_stop',)

@admin.register(PermissionHistory)
class PermissionHistoryDefined(admin.ModelAdmin):
    readonly_fields = ('permission_name', 'permission_start', 'permission_stop', 'permission_owner', )
    list_display = ('permission_name', 'permission_start', 'permission_stop', 'permission_owner', )
    search_fields = ('permission_owner', 'permission_name')
    list_filter = ('permission_owner', 'permission_name')


admin.site.unregister(Group)
admin.site.site_header = "Hararii TVET Agency Digital Attendance Sheet 爐"
