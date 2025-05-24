# academy/views/student_views.py

from django.shortcuts import render, redirect, get_object_or_404
from academy.models import Student, Attendance, Assignment, Exam, Classroom
from academy.views.views_utils import calculate_mileage_from_rules
from django.contrib.auth.decorators import login_required

def home_redirect(request):
    return redirect('student_login_teacher')

def student_login_teacher(request):
    return render(request, 'academy/student_login_teacher.html')

def student_select(request):
    teacher = request.GET.get('teacher')
    classrooms = Classroom.objects.filter(teacher_name=teacher)
    students = Student.objects.filter(classroom__in=classrooms).order_by('name')
    return render(request, 'academy/student_select.html', {'students': students, 'teacher': teacher})

def student_auth(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    error = None
    if request.method == 'POST':
        password = request.POST.get('password')
        if password == student.password:
            request.session['student_id'] = student.id
            return redirect('student_my_page')
        else:
            error = "비밀번호가 틀렸습니다."
    return render(request, 'academy/student_auth.html', {'student': student, 'error': error})

def student_my_page(request):
    student_id = request.session.get('student_id')
    if not student_id:
        return redirect('student_login_teacher')
    student = get_object_or_404(Student, pk=student_id)
    attendances = Attendance.objects.filter(student=student)
    assignments = Assignment.objects.filter(student=student)
    exams = Exam.objects.filter(student=student)
    total_points = calculate_mileage_from_rules(student)
    return render(request, 'academy/student_public_detail.html', {
        'student': student,
        'attendances': attendances,
        'assignments': assignments,
        'exams': exams,
        'total_points': total_points,
    })

def student_public_detail(request, pk):
    student = get_object_or_404(Student, pk=pk)
    attendances = Attendance.objects.filter(student=student).order_by('-date')
    assignments = Assignment.objects.filter(student=student)
    exams = Exam.objects.filter(student=student).order_by('-exam_date')
    total_points = calculate_mileage_from_rules(student)
    return render(request, 'academy/student_public_detail.html', {
        'student': student,
        'attendances': attendances,
        'assignments': assignments,
        'exams': exams,
        'total_points': total_points,
    })

def student_detail(request, pk):
    # (같은 템플릿 재사용 or 차이 있으면 따로 작성)
    return student_public_detail(request, pk)

def student_list(request):
    students = Student.objects.all()
    return render(request, 'academy/student_list.html', {'students': students})

