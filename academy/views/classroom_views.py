# academy/views/classroom_views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from academy.forms import ClassroomForm
from academy.models import Classroom, Student
from django.db import IntegrityError


@login_required
def classroom_create(request):
    error = None
    if request.method == 'POST':
        form = ClassroomForm(request.POST)
        if form.is_valid():
            classroom = form.save(commit=False)
            classroom.teacher_user = request.user
            classroom.teacher_name = request.user.username
            try:
                classroom.save()
                return redirect('teacher_dashboard')
            except IntegrityError:
                error = "같은 이름의 반이 이미 존재합니다."
    else:
        form = ClassroomForm()

    return render(request, 'academy/classroom_form.html', {'form': form, 'error': error})


@login_required
def delete_classroom(request, classroom_id):
    classroom = get_object_or_404(Classroom, id=classroom_id, teacher_user=request.user)

    default_classroom, _ = Classroom.objects.get_or_create(
        name='미정',
        teacher_user=request.user,
        defaults={'teacher_name': request.user.username}
    )

    if request.method == 'POST':
        Student.objects.filter(classroom=classroom).update(classroom=default_classroom)
        classroom.delete()
        return redirect('teacher_dashboard')

    return render(request, 'academy/confirm_delete_classroom.html', {'classroom': classroom})