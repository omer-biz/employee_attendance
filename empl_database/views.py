from datetime import date, datetime

from django.shortcuts import render
from django.http import HttpResponse

from .models import Employee, Attendance

def index(request):
    return render(request, 'index.html')

def search(request):
    # Get the employee with id_number
    try:
        query = request.GET.get('q')
        employee = Employee.objects.get(id_number=query)
        atn_const = employee.attendance_constraint
    except:
        # return render(request, 'not_found.html')
        return HttpResponse("Not found")

    # if the employee an attendance already get
    # or create a new one
    try:
        attendance = Attendance.objects.get(employee=employee, 
                                            date=date.today())
    except:
        attendance = Attendance.objects.create(date=date.today(), 
                                               employee=employee)

    now = datetime.now().time()

    # Morning Entry Constraint
    if now >= atn_const.mg_en_str and now <= atn_const.mg_en_stp:

        if attendance.morning_entry == None:
            attendance.morning_entry = datetime.now().time()
            attendance.save()
            return HttpResponse(f"Morning Entry Attendance Taken")
        else:
            return HttpResponse("Morning Entry Attendance Already Taken")

    # Morning Exit Constraint
    elif now >= atn_const.mg_ex_str and now <= atn_const.mg_ex_stp:

        if attendance.morning_exit == None:
            attendance.morning_exit = datetime.now().time()
            attendance.save()
            return HttpResponse(f"Morning Exit Attendance Taken")
        else:
            return HttpResponse(f"Morning Exit Attendance Already Taken")

    # Afternoon Entry Constraint
    elif now >= atn_const.an_en_str and now <= atn_const.an_en_stp:

        if attendance.afternoon_entry == None:
            attendance.afternoon_entry = datetime.now().time()
            attendance.save()
            return HttpResponse("Afternoon Entry Attendance Taken")
        else:
            return HttpResponse("Afternoon Entry Attendance Already Taken")

    # Afternoon Exit Constraint
    elif now >= atn_const.an_ex_str and now <= atn_const.an_ex_stp:

        if attendance.afternoon_exit == None:
            attendance.afternoon_exit = datetime.now().time()
            attendance.save()
            return HttpResponse("Afternoon Exit Attendance Taken")
        else:
            return HttpResponse("Afternoon Exit Attendance Already Taken")

    # This is not the time to take attendances
    else:
        return HttpResponse(f"You cannot take attendance now")
