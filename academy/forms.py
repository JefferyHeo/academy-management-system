from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms.widgets import DateInput
from .models import Student, Attendance, Assignment, Exam, MileageRule

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'contact', 'grade', 'classroom', 'password']
        widgets = {
            'password': forms.PasswordInput(attrs={'maxlength': 4})
        }

    def __init__(self, *args, **kwargs):
        teacher = kwargs.pop('teacher', None)
        super().__init__(*args, **kwargs)
        if teacher:
            self.fields['classroom'].queryset = Classroom.objects.filter(teacher_user=teacher)

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['student', 'date', 'status', 'reason']
        widgets = {
            'student': forms.HiddenInput(),
            'date': DateInput(attrs={'type': 'date'}),
            'reason': forms.Textarea(attrs={'rows': 2, 'placeholder': '사유를 입력하세요'}),
        }


class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['student', 'title', 'submitted', 'date']
        widgets = {
            'student':forms.HiddenInput(),
            'date': DateInput(attrs={'type': 'date'}),
        }

class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ['student', 'exam_date', 'subject', 'score']
        widgets = {
            'exam_date': DateInput(attrs={'type': 'date'}),
        }

class MileageRuleForm(forms.ModelForm):
    score_value = forms.IntegerField(required=False, label="점수")
    score_operator = forms.ChoiceField(
        required=False,
        label="조건",
        choices=[('>=', '이상'), ('<', '미만'), ('==', '맞을 시')]
    )

    condition = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = MileageRule
        fields = ['category', 'condition', 'points']
        widgets = {
            'condition': forms.HiddenInput()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        category = self.initial.get('category') or self.data.get('category')
        condition = self.initial.get('condition') or self.data.get('condition')

        # 기존 condition 값에서 시험 점수 조건 분해
        if category == 'exam' and condition and condition.startswith("score"):
            import re
            match = re.match(r'score([<>=]=?)(\d+)', condition)
            if match:
                self.fields['score_operator'].initial = match.group(1)
                self.fields['score_value'].initial = match.group(2)

    def clean(self):
        cleaned_data = super().clean()
        category = cleaned_data.get('category')

        if category == 'exam':
            op = self.data.get('score_operator')
            val = self.data.get('score_value')

            if not op:
                self.add_error('score_operator', '조건을 선택하세요.')
            if not val:
                self.add_error('score_value', '점수를 입력하세요.')

            if op and val:
                cleaned_data['condition'] = f"score{op}{val}"
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)

        # description 자동 설정
        if instance.category == 'attendance':
            label = {'present': '출석', 'late': '지각', 'absent': '결석'}.get(instance.condition, instance.condition)
            instance.description = f"{label} 시"
        elif instance.category == 'assignment':
            instance.description = "과제 제출 시" if instance.condition == 'submitted' else "과제 미제출 시"
        elif instance.category == 'exam':
            instance.description = f"시험 점수 {instance.condition[5:]} 시"

        if commit:
            instance.save()
        return instance

class TeacherSignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

from django import forms
from .models import Classroom

class ClassroomForm(forms.ModelForm):
    class Meta:
        model = Classroom
        fields = ['name']
