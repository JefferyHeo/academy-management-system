from django.contrib import admin
from .models import Classroom, Student, Attendance, Assignment, Exam

admin.site.register(Classroom)
admin.site.register(Student)
admin.site.register(Attendance)
admin.site.register(Assignment)
admin.site.register(Exam)

