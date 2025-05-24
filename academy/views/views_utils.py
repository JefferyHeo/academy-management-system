# academy/views/views_utils.py

from academy.models import Attendance, Assignment, Exam, MileageRule


def calculate_mileage_from_rules(student):
    total_points = 0
    teacher_user = student.classroom.teacher_user
    rules = MileageRule.objects.filter(teacher=teacher_user)

    for rule in rules:
        if rule.category == 'attendance':
            for a in Attendance.objects.filter(student=student):
                if a.status == rule.condition:
                    total_points += rule.points
        elif rule.category == 'assignment':
            for asg in Assignment.objects.filter(student=student):
                if rule.condition == 'submitted' and asg.submitted:
                    total_points += rule.points
                elif rule.condition == 'not_submitted' and not asg.submitted:
                    total_points += rule.points
        elif rule.category == 'exam':
            for e in Exam.objects.filter(student=student):
                cond = rule.condition
                try:
                    if cond.startswith("score>=") and e.score >= float(cond.split(">=")[1]):
                        total_points += rule.points
                    elif cond.startswith("score>") and e.score > float(cond.split(">")[1]):
                        total_points += rule.points
                    elif cond.startswith("score==") and e.score == float(cond.split("==")[1]):
                        total_points += rule.points
                    elif cond.startswith("score<=") and e.score <= float(cond.split("<=")[1]):
                        total_points += rule.points
                    elif cond.startswith("score<") and e.score < float(cond.split("<")[1]):
                        total_points += rule.points
                except (ValueError, IndexError):
                    continue
    return total_points
