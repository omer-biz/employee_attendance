from datetime import date, datetime, timedelta
from django.shortcuts import render

from .models import Employee, Attendance, Permission, PermissionHistory


def calc_absent_dates(empl: Employee, start: date, end: date):
    hit = 0
    domain = 0

    atns = Attendance.objects.filter(employee=empl, date__range=(start, end))

    latest_absents = []
    for atn in atns:
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

    return percent, latest_absents

def check_permission(empl: Employee):
    today = date.today()
    has_permission = False

    if empl.permission != None:
        if today >= empl.permission.permission_start and today <= empl.permission.permission_stop:
            has_permission = True

        else:
            permission_history = PermissionHistory.objects.create(
                permission_start=empl.permission.permission_start,
                permission_stop=empl.permission.permission_stop,
                permission_name=empl.permission.permission_name,
                permission_owner=empl,
            )
            permission_history.save()

            perm = Permission.objects.get(id=empl.permission.id)

            empl.permission = None
            empl.save()

            perm.delete()

    return has_permission

def create_attendance():
    employees = Employee.objects.all()
    today = date.today()

    for empl in employees:
        if check_permission(empl=empl) != True:
            if Attendance.objects.filter(employee=empl, date=today).count() == 0:
                Attendance.objects.create(date=date.today(), employee=empl)

def index(request):
    today = date.today()
    if today.weekday() == 5 or today.weekday() == 6:
        return render(request, 'index.html', context={
            'msg': 'You can not take attendance on weekends',
            'hint_color': '#ff9800'
        })
    create_attendance()
    return render(request, 'index.html', context={
    })

def generate_salary(request):

    try:
        start = date.fromisoformat(request.GET.get('start'))
        end = date.fromisoformat(request.GET.get('end'))

        if start > end:
            raise Exception

        employees = Employee.objects.all()
        empls_salary = {}
        for empl in employees:
            percent, _ = calc_absent_dates(empl=empl, start=start, end=end)
            empls_salary[empl.full_name] = []
            empls_salary[empl.full_name].append((percent * empl.salary)/100)
            empls_salary[empl.full_name].append(100 - percent)

        return render(request, 'sheet.html', context={
            'employees_salary': 'empls_salary',
        })
    except:
        return render(request, 'salary_sheet.html', context={
            'msg': 'Please specify date (properly)',
            'hint_color': '#ff9800'
        })


def generate_sheet(request):
    try:
        start = date.fromisoformat(request.GET.get('start'))
        end = date.fromisoformat(request.GET.get('end'))

        if start > end:
            raise Exception

        employees = Employee.objects.all()

        absent_sheet = {}
        for empl in employees:
            atns = Attendance.objects.filter(
                employee=empl, date__range=(start, end))

            if atns.count() == 0:
                continue

            absent_sheet[empl.full_name] = {}

            for atn in atns:
                cur_date = atn.date.strftime('%b, %d (%A)')
                absent_sheet[empl.full_name][cur_date] = []

                if atn.morning_entry == None:
                    absent_sheet[empl.full_name][cur_date].append(atn.date.strftime('Morning Entry'))

                if atn.morning_exit == None:
                    absent_sheet[empl.full_name][cur_date].append(atn.date.strftime('Morning Exit'))

                if atn.afternoon_entry == None:
                    absent_sheet[empl.full_name][cur_date].append(atn.date.strftime('Afternoon Entry'))

                if atn.afternoon_exit == None:
                    absent_sheet[empl.full_name][cur_date].append(atn.date.strftime('Afternoon Exit'))


        return render(request, 'sheet.html', context={
            'absent_sheet': absent_sheet,
            'start_of_month': start.strftime('%b, %d %Y'),
            'today': end.strftime('%b, %d %Y'),
        })
    except:
        return render(request, 'absent_sheet.html', context={
            'msg': 'Please specify date (properly)',
            'hint_color': '#ff9800',
        })


def search(request):
    hint_color_red = '#f44336'
    hint_color_green = '#04AA6D'
    hint_color_blue = '#2196F3'
    hint_color_yellow = '#ff9800'

    today = date.today()

    if today.weekday() == 5 or today.weekday() == 6:
        return render(request, 'index.html', context={
            'msg': 'You can not take attendance on weekends',
            'hint_color': hint_color_blue,
        })

    try:
        query = request.GET.get('q')
        employee = Employee.objects.get(id_number=query)
        atn_const = employee.attendance_constraint
    except:
        return render(request,
                      'index.html',
                       context={'msg': 'Employee Not Found',
                                'hint_color':hint_color_red})

    now = datetime.now().time()

    if check_permission(empl=employee) != True:
        try:
            attendance = Attendance.objects.get(employee=employee,
                                                date=date.today())
        except:
            attendance = Attendance.objects.create(date=date.today(),
                                                   employee=employee)
        # attendance = Attendance.objects.get_or_create(date=today, employee=employee)
        if now >= atn_const.mg_en_str and now <= atn_const.mg_en_stp:

            if attendance.morning_entry == None:
                attendance.morning_entry = datetime.now().time()
                attendance.save()
                msg = f"Morning Entry Attendance Taken"
                hint_color = hint_color_green
            else:
                msg = "Morning Entry Attendance Already Taken"
                hint_color = hint_color_blue

        elif now >= atn_const.mg_ex_str and now <= atn_const.mg_ex_stp:

            if attendance.morning_exit == None:
                attendance.morning_exit = datetime.now().time()
                attendance.save()
                msg = f"Morning Exit Attendance Taken"
                hint_color = hint_color_green
            else:
                msg = f"Morning Exit Attendance Already Taken"
                hint_color = hint_color_blue

        elif now >= atn_const.an_en_str and now <= atn_const.an_en_stp:

            if attendance.afternoon_entry == None:
                attendance.afternoon_entry = datetime.now().time()
                attendance.save()
                msg = "Afternoon Entry Attendance Taken"
                hint_color = hint_color_green
            else:
                msg = "Afternoon Entry Attendance Already Taken"
                hint_color = hint_color_blue

        elif now >= atn_const.an_ex_str and now <= atn_const.an_ex_stp:

            if attendance.afternoon_exit == None:
                attendance.afternoon_exit = datetime.now().time()
                attendance.save()
                msg = "Afternoon Exit Attendance Taken"
                hint_color = hint_color_green
            else:
                msg = "Afternoon Exit Attendance Already Taken"
                hint_color = hint_color_blue

        else:
            msg = f"You cannot take attendance now"
            hint_color = hint_color_red
    else:
        msg = f"This employee is on permission"
        hint_color = hint_color_yellow


    today = date.today()
    odb_today = today - timedelta(days=1)
    start_of_month = date(today.year, today.month, 1)
    percent, latest_absents = calc_absent_dates(empl=employee, start=start_of_month, end=odb_today)

    return render(request, 'index.html', context={
        'employee': employee, 
        'msg': msg,
        'percent': f"{percent:3.2f}",
        'latest_absents': latest_absents[:3],
        'hint_color': hint_color,
    })
