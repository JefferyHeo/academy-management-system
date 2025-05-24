# academy/views/auth_views.py

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from academy.forms import TeacherSignupForm
from academy.models import MileageRule
from academy.views.views_utils import calculate_mileage_from_rules


def teacher_login(request):
    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('teacher_dashboard')
        else:
            error = '아이디 또는 비밀번호가 올바르지 않습니다.'
    return render(request, 'academy/teacher_login.html', {'error': error})

def teacher_logout(request):
    logout(request)
    return redirect('teacher_login')

def create_default_mileage_rules(teacher_user):
    default_rules = [
        {'category': 'attendance', 'condition': 'present', 'points': 5, 'description': '출석 시'},
        {'category': 'attendance', 'condition': 'late', 'points': -3, 'description': '지각 시'},
        {'category': 'attendance', 'condition': 'absent', 'points': -10, 'description': '결석 시'},
        {'category': 'assignment', 'condition': 'submitted', 'points': 7, 'description': '과제 제출 시'},
        {'category': 'assignment', 'condition': 'not_submitted', 'points': -5, 'description': '과제 미제출 시'},
        {'category': 'exam', 'condition': 'score>=100', 'points': 15, 'description': '시험 만점 시'},
    ]
    for rule in default_rules:
        MileageRule.objects.create(teacher=teacher_user, **rule)

def teacher_signup(request):
    if request.method == 'POST':
        form = TeacherSignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = True
            user.save()
            create_default_mileage_rules(user)
            login(request, user)
            return redirect('teacher_dashboard')
    else:
        form = TeacherSignupForm()
    return render(request, 'academy/teacher_signup.html', {'form': form})
