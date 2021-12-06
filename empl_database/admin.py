from django.contrib import admin
from django.contrib.auth.models import Group
from django.db import models
from django.forms import NumberInput

from .models import Employee

@admin.register(Employee)
class EmployeeDefined(admin.ModelAdmin):
    list_display = ('full_name', 'occupation', 'sex', 'id_number')
    list_filter = ('occupation', 'sex')
    search_fields = ('full_name', 'occupation', 'id_number')
    formfield_overrides = {
        models.IntegerField: {'widget': NumberInput(attrs={'size': '20'})}
    }


admin.site.unregister(Group)

admin.site.site_header = "TVET Agency"
