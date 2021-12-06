from django.shortcuts import render
from django.http import HttpResponse
from .models import Employee

def index(request):
    return HttpResponse("Hello, World")

def search(request, id_number):
    employee = Employee.objects.get(id_number=id_number)
    return HttpResponse(f"Hello {employee.full_name}")
