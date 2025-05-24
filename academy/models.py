from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Classroom(models.Model):
    name = models.CharField(max_length=100)
    teacher_name = models.CharField(max_length=100)
    teacher_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.teacher_user.username if self.teacher_user else '미정'})"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['teacher_user', 'name'], name='unique_classroom_per_teacher')
        ]

class Student(models.Model):
    name = models.CharField(max_length=100)
    contact = models.CharField(max_length=100)
    grade = models.IntegerField()
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    password = models.CharField(max_length=4)  # 4자리 숫자 비밀번호

    def __str__(self):
        return self.name

class Attendance(models.Model):
    STATUS_CHOICES = [
        ('present', '출석'),
        ('late', '지각'),
        ('absent', '결석'),
    ]
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    reason = models.TextField(blank=True)

    def __str__(self):
        return f'{self.student.name} - {self.date} ({self.status})'


class Assignment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    submitted = models.BooleanField(default=False)
    points = models.IntegerField(default=0)
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return f'{self.student.name} - {self.title}'

class Exam(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    exam_date = models.DateField(default=timezone.now)
    subject = models.CharField(max_length=100)
    score = models.FloatField()

    def __str__(self):
        return f'{self.student.name} - {self.subject} ({self.exam_date})'

class MileageRule(models.Model):
    CATEGORY_CHOICES = [
        ('attendance', '출결'),
        ('assignment', '과제'),
        ('exam', '시험'),
    ]
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    condition = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    points = models.IntegerField()

    def __str__(self):
        return f"[{self.get_category_display()}] {self.description} ({self.points}점)"
