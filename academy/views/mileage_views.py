# academy/views/mileage_views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from academy.models import MileageRule, Attendance, Assignment, Exam


@login_required
def mileage_rule_list(request):
    rules = MileageRule.objects.filter(teacher=request.user)
    return render(request, 'academy/mileage_rule_list.html', {'rules': rules})

@login_required
def mileage_rule_create(request):
    from academy.forms import MileageRuleForm
    if request.method == 'POST':
        form = MileageRuleForm(request.POST)
        if form.is_valid():
            rule = form.save(commit=False)
            rule.teacher = request.user
            rule.save()
            return redirect('mileage_rule_list')
    else:
        form = MileageRuleForm()
    return render(request, 'academy/mileage_rule_form.html', {'form': form})

@login_required
def mileage_rule_edit(request, rule_id):
    from academy.forms import MileageRuleForm
    rule = get_object_or_404(MileageRule, pk=rule_id)
    if request.method == 'POST':
        form = MileageRuleForm(request.POST, instance=rule)
        if form.is_valid():
            form.save()
            return redirect('mileage_rule_list')
    else:
        form = MileageRuleForm(instance=rule)
    return render(request, 'academy/mileage_rule_form.html', {
        'form': form,
        'rule': rule,
        'action': '수정',
    })

@login_required
def delete_mileage_rule(request, rule_id):
    rule = get_object_or_404(MileageRule, id=rule_id, teacher=request.user)
    if request.method == 'POST':
        rule.delete()
        return redirect('mileage_rule_list')
    return render(request, 'academy/confirm_delete_mileage_rule.html', {'rule': rule})
