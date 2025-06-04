# academy/views/attendance_views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from datetime import date
from django.urls import reverse
import calendar
from academy.models import Attendance, Student
from academy.forms import AttendanceForm
from academy.views.views_utils import calculate_mileage_from_rules


@login_required
def attendance_create(request):
    student_id = request.GET.get('student')
    if not student_id:
        return redirect('teacher_dashboard')

    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            date_value = form.cleaned_data['date']
            status = form.cleaned_data['status']
            reason = form.cleaned_data.get('reason', '')
            attendance, created = Attendance.objects.get_or_create(
                student_id=student_id,
                date=date_value,
                defaults={'status': status, 'reason': reason}
            )
            if not created:
                attendance.status = status
                attendance.reason = reason
                attendance.save()
            return redirect(reverse('attendance_list') + f'?student={student_id}')
    else:
        date_str = request.GET.get('date')
        try:
            selected_date = date.fromisoformat(date_str) if date_str else date.today()
        except:
            selected_date = date.today()

        try:
            attendance = Attendance.objects.get(student_id=student_id, date=selected_date)
            form = AttendanceForm(initial={
                'date': attendance.date,
                'status': attendance.status,
                'reason': attendance.reason,
                'student': student_id,
            })
        except Attendance.DoesNotExist:
            form = AttendanceForm(initial={
                'date': selected_date,
                'student': student_id,
            })

    return render(request, 'academy/attendance_form.html', {
        'form': form,
        'student_id': student_id
    })

@login_required
def attendance_list(request):
    student_id = request.GET.get('student')
    student = get_object_or_404(Student, pk=student_id)
    today = date.today()
    year = int(request.GET.get('year', today.year))
    month = int(request.GET.get('month', today.month))
    attendances = Attendance.objects.filter(
        student_id=student_id, date__year=year, date__month=month
    )
    attendance_dict = {a.date.day: a.get_status_display() for a in attendances}
    attendance_reasons = {a.date.day: a.reason for a in attendances}
    cal = calendar.Calendar(firstweekday=6)
    month_days = cal.monthdayscalendar(year, month)
    prev_month, prev_year = (12, year - 1) if month == 1 else (month - 1, year)
    next_month, next_year = (1, year + 1) if month == 12 else (month + 1, year)
    context = {
        'student': student,
        'year': year,
        'month': month,
        'month_days': month_days,
        'attendance_dict': attendance_dict,
        'attendance_reasons': attendance_reasons,
        'prev_year': prev_year,
        'prev_month': prev_month,
        'next_year': next_year,
        'next_month': next_month,
    }
    return render(request, 'academy/attendance_list.html', context)

@login_required
def attendance_calendar(request):
    student_id = request.GET.get('student')
    student = get_object_or_404(Student, pk=student_id)
    today = date.today()
    year = int(request.GET.get('year', today.year))
    month = int(request.GET.get('month', today.month))
    attendances = Attendance.objects.filter(
        student_id=student_id, date__year=year, date__month=month
    )
    attendance_dict = {a.date.day: a.get_status_display() for a in attendances}
    cal = calendar.Calendar(firstweekday=6)
    month_days = cal.monthdayscalendar(year, month)
    context = {
        'student': student,
        'year': year,
        'month': month,
        'month_days': month_days,
        'attendance_dict': attendance_dict,
    }
    return render(request, 'academy/attendance_calendar.html', context)
