# academy/views/teacher_views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from academy.models import Student, Classroom
from academy.forms import StudentForm
from academy.views.views_utils import calculate_mileage_from_rules

@login_required
def teacher_dashboard(request):
    classrooms = Classroom.objects.filter(teacher_user=request.user)
    students = Student.objects.filter(classroom__in=classrooms).order_by('classroom__name', 'name')
    return render(request, 'academy/teacher_dashboard.html', {
        'students': students,
        'classrooms': classrooms,
    })

@login_required
def student_create(request):
    if request.method == 'POST':
        form = StudentForm(request.POST, teacher=request.user)
        if form.is_valid():
            student = form.save(commit=False)
            if student.classroom.teacher_user == request.user:
                student.save()
                request.session['student_created'] = True
                return redirect('student_create_done')
            else:
                form.add_error(None, "해당 클래스는 선생님의 반이 아닙니다.")
    else:
        form = StudentForm(teacher=request.user)
    return render(request, 'academy/student_form.html', {
        'form': form,
        'action': '등록',
    })

@login_required
def student_create_done(request):
    if not request.session.get('student_created'):
        return redirect('student_create')
    request.session['student_created'] = False
    return render(request, 'academy/student_create_done.html')

@login_required
def student_edit(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    if student.classroom.teacher_user != request.user:
        return redirect('teacher_dashboard')
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student, teacher=request.user)
        if form.is_valid():
            form.save()
            return redirect('teacher_dashboard')
    else:
        form = StudentForm(instance=student, teacher=request.user)
    return render(request, 'academy/student_form.html', {'form': form})

@login_required
def classroom_list(request):
    classrooms = Classroom.objects.filter(teacher_user=request.user)
    return render(request, 'academy/classroom_list.html', {'classrooms': classrooms})
