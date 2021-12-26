from datetime import date, datetime
from django.shortcuts import render

from .models import Employee, Attendance, PermissionHistory

def index(request):
    return render(request, 'index.html')

def search(request):
    hint_color_red = '#f44336'
    hint_color_green = '#04AA6D'
    hint_color_blue = '#2196F3'
    # hint_color_yellow = '#ff9800'

    today = date.today()
    start_of_month = date(today.year, today.month, 1)

    # if today.weekday() == 5 or today.weekday() == 6:
    #     return render(request, 'index.html', context={
    #         'msg': 'You can not take attendance on weekends',
    #         'hint_color': hint_color_blue,
    #     })

    # Get the employee with id_number
    try:
        query = request.GET.get('q')
        employee = Employee.objects.get(id_number=query)
        atn_const = employee.attendance_constraint
    except:
        return render(request, 
                      'index.html', 
                       context={'msg': 'Employee Not Found',
                                'hint_color':hint_color_red})

    try:
        attendance = Attendance.objects.get(employee=employee, 
                                            date=date.today())
    except:
        attendance = Attendance.objects.create(date=date.today(), 
                                               employee=employee)

    if employee.permission != None:
        # check if the permission is expried
        if today >= employee.permission.permission_start and today <= employee.permission.permission_stop:
            msg = 'This employee is on permission'
            hint_color = hint_color_blue
        # if expired move to permission history and set to null
        else:
            permission_history = PermissionHistory.objects.create(
                permission_start=employee.permission.permission_start,
                permission_stop=employee.permission.permission_stop,
                permission_name=employee.permission.permission_name,
                permission_owner=employee,
            )
            permission_history.save()

            employee.permission = None
            employee.save()

    now = datetime.now().time()
    # Morning Entry Constraint
    if now >= atn_const.mg_en_str and now <= atn_const.mg_en_stp:

        if attendance.morning_entry == None:
            attendance.morning_entry = datetime.now().time()
            attendance.save()
            msg = f"Morning Entry Attendance Taken"
            hint_color = hint_color_green
        else:
            msg = "Morning Entry Attendance Already Taken"
            hint_color = hint_color_blue

    # Morning Exit Constraint
    elif now >= atn_const.mg_ex_str and now <= atn_const.mg_ex_stp:

        if attendance.morning_exit == None:
            attendance.morning_exit = datetime.now().time()
            attendance.save()
            msg = f"Morning Exit Attendance Taken"
            hint_color = hint_color_green
        else:
            msg = f"Morning Exit Attendance Already Taken"
            hint_color = hint_color_blue

    # Afternoon Entry Constraint
    elif now >= atn_const.an_en_str and now <= atn_const.an_en_stp:

        if attendance.afternoon_entry == None:
            attendance.afternoon_entry = datetime.now().time()
            attendance.save()
            msg = "Afternoon Entry Attendance Taken"
            hint_color = hint_color_green
        else:
            msg = "Afternoon Entry Attendance Already Taken"
            hint_color = hint_color_blue

    # Afternoon Exit Constraint
    elif now >= atn_const.an_ex_str and now <= atn_const.an_ex_stp:

        if attendance.afternoon_exit == None:
            attendance.afternoon_exit = datetime.now().time()
            attendance.save()
            msg = "Afternoon Exit Attendance Taken"
            hint_color = hint_color_green
        else:
            msg = "Afternoon Exit Attendance Already Taken"
            hint_color = hint_color_blue

    # This is not the time to take attendances
    else:
        msg = f"You cannot take attendance now"
        hint_color = hint_color_red


    atns = Attendance.objects.filter(employee=employee)
    hit = 0
    domain = 0
    latest_absents = []
    for atn in atns:
        if atn.date >= start_of_month and atn.date < today:
            domain += 1

            if atn.morning_entry == None:
                latest_absents.append(atn.date.strftime('%b, %d (%A Morning Entry)'))
                hit += 1
            if atn.morning_exit == None:
                latest_absents.append(atn.date.strftime('%b, %d (%A Morning Exit)'))
                hit += 1

            if atn.afternoon_entry == None:
                latest_absents.append(atn.date.strftime('%b, %d (%A Afternoon Entry)'))
                hit += 1
            if atn.afternoon_exit == None:
                latest_absents.append(atn.date.strftime('%b, %d (%A Afternoon Exit)'))
                hit += 1

    percent = 100
    if domain != 0:
        percent = 100 - (hit * 100 / (domain * 4))

    return render(request, 'index.html', context={
        'employee': employee, 
        'msg': msg,
        'percent': f"{percent:3.2f}",
        'latest_absents': latest_absents[:5],
        'hint_color': hint_color,
    })
