from django.urls import path
from . import views

urlpatterns = [
    # 🌐 홈 리디렉션
    path('', views.home_redirect, name='home_redirect'),

    # 🧑‍🎓 학생 로그인/마이페이지 흐름
    path('student/login/', views.student_login_teacher, name='student_login_teacher'),
    path('student/select/', views.student_select, name='student_select'),
    path('student/auth/<int:student_id>/', views.student_auth, name='student_auth'),
    path('student/me/', views.student_my_page, name='student_my_page'),
    path('student/<int:pk>/', views.student_public_detail, name='student_public_detail'),

    # 👨‍🏫 교사용 학생 관리
    path('teacher/student/add/', views.student_create, name='student_create'),
    path('teacher/student/add/done/', views.student_create_done, name='student_create_done'),
    path('teacher/student/<int:student_id>/edit/', views.student_edit, name='student_edit'),
    path('teacher/students/', views.student_list, name='student_list'),

    # 🏫 반 등록
    path('teacher/classroom/add/', views.classroom_create, name='classroom_create'),

    # 📅 출결
    path('attendance/', views.attendance_list, name='attendance_list'),
    path('attendance/create/', views.attendance_create, name='attendance_create'),
    path('attendance/calendar/', views.attendance_calendar, name='attendance_calendar'),

    # 📝 과제
    path('assignments/', views.assignment_list, name='assignment_list'),
    path('assignments/create/', views.assignment_create, name='assignment_create'),
    path('assignments/<int:assignment_id>/toggle/', views.assignment_toggle, name='assignment_toggle'),

    # 🧪 시험
    path('exams/', views.exam_list, name='exam_list'),
    path('exams/create/', views.exam_create, name='exam_create'),
    path('exams/<int:exam_id>/edit/', views.exam_edit, name='exam_edit'),

    # 🎯 마일리지 룰
    path('teacher/mileage-rules/', views.mileage_rule_list, name='mileage_rule_list'),
    path('teacher/mileage-rules/create/', views.mileage_rule_create, name='mileage_rule_create'),
    path('teacher/mileage-rules/<int:rule_id>/edit/', views.mileage_rule_edit, name='mileage_rule_edit'),

    # 👨‍🏫 선생님 인증 + 대시보드
    path('teacher/login/', views.teacher_login, name='teacher_login'),
    path('teacher/logout/', views.teacher_logout, name='teacher_logout'),
    path('teacher/signup/', views.teacher_signup, name='teacher_signup'),
    path('teacher/', views.teacher_dashboard, name='teacher_dashboard'),
]
