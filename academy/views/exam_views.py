# academy/views/exam_views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from academy.models import Exam, Student
from academy.forms import ExamForm
from django.urls import reverse

@login_required
def exam_create(request):
    student_id = request.GET.get('student') or request.POST.get('student')
    if not student_id:
        return redirect('teacher_dashboard')
    if request.method == 'POST':
        form = ExamForm(request.POST)
        if form.is_valid():
            exam = form.save(commit=False)
            exam.student_id = student_id
            exam.save()
            return redirect(reverse('exam_list') + f'?student={student_id}')  # 수정됨
    else:
        form = ExamForm()
    return render(request, 'academy/exam_form.html', {
        'form': form,
        'student_id': student_id
    })

@login_required
def exam_edit(request, exam_id):
    exam = get_object_or_404(Exam, pk=exam_id)
    if exam.student.classroom.teacher_user != request.user:
        return redirect('teacher_dashboard')
    if request.method == 'POST':
        form = ExamForm(request.POST, instance=exam)
        if form.is_valid():
            form.save()
            return redirect(reverse('exam_list') + f'?student={exam.student.id}')  # 수정됨
    else:
        form = ExamForm(instance=exam)
    return render(request, 'academy/exam_form.html', {
        'form': form,
        'student_id': exam.student.id
    })

@login_required
def exam_list(request):
    student_id = request.GET.get('student')
    student = None
    if student_id:
        exams = Exam.objects.filter(student_id=student_id).order_by('-exam_date')
        student = get_object_or_404(Student, pk=student_id)
    else:
        exams = Exam.objects.select_related('student').order_by('-exam_date')
    return render(request, 'academy/exam_list.html', {
        'exams': exams,
        'student': student
    })
