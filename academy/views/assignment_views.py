# academy/views/assignment_views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from academy.models import Student, Classroom, Assignment
from academy.forms import AssignmentForm
from academy.views.views_utils import calculate_mileage_from_rules


@login_required
def assignment_create(request):
    student_id = request.GET.get('student') or request.POST.get('student')
    if not student_id:
        return redirect('teacher_dashboard')
    if request.method == 'POST':
        form = AssignmentForm(request.POST)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.student_id = student_id
            assignment.save()
            return redirect(f'/assignments/?student={student_id}')
    else:
        form = AssignmentForm()
    return render(request, 'academy/assignment_form.html', {
        'form': form,
        'student_id': student_id
    })

@login_required
def assignment_list(request):
    student_id = request.GET.get('student')
    student = None
    if student_id:
        assignments = Assignment.objects.filter(student_id=student_id).order_by('-id')
        student = get_object_or_404(Student, pk=student_id)
    else:
        assignments = Assignment.objects.select_related('student').order_by('-id')
    return render(request, 'academy/assignment_list.html', {
        'assignments': assignments,
        'student': student
    })

@login_required
def assignment_toggle(request, assignment_id):
    assignment = get_object_or_404(Assignment, pk=assignment_id)
    if assignment.student.classroom.teacher_user != request.user:
        return redirect('teacher_dashboard')
    assignment.submitted = not assignment.submitted
    assignment.save()
    return redirect(f'/assignments/?student={assignment.student.id}')
