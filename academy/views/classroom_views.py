# academy/views/classroom_views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from academy.forms import ClassroomForm
from academy.views.views_utils import calculate_mileage_from_rules


@login_required
def classroom_create(request):
    if request.method == 'POST':
        form = ClassroomForm(request.POST)
        if form.is_valid():
            classroom = form.save(commit=False)
            classroom.teacher_user = request.user
            classroom.teacher_name = request.user.username
            classroom.save()
            return redirect('teacher_dashboard')
    else:
        form = ClassroomForm()
    return render(request, 'academy/classroom_form.html', {'form': form})
