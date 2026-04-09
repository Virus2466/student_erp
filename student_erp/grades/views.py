from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Grade
from .forms import GradeForm

@login_required
def grade_list(request):
    if request.user.role == 'student':
        try:
            student = request.user.student_profile
            grades = Grade.objects.filter(student=student)
        except:
            grades = Grade.objects.none()
    else:
        grades = Grade.objects.all()
    
    return render(request, 'grades/list.html', {
        'grades': grades
    })

@login_required
def add_grade(request):
    if request.user.role not in ['admin', 'teacher']:
        messages.error(request, 'You do not have permission to add grades.')
        return redirect('grade_list')
    
    if request.method == 'POST':
        form = GradeForm(request.POST)
        if form.is_valid():
            grade = form.save()
            messages.success(request, f'Grade added successfully for {grade.student.user.get_full_name()}')
            return redirect('grade_list')
    else:
        form = GradeForm()
    
    return render(request, 'grades/add.html', {'form': form})

@login_required
def edit_grade(request, pk):
    if request.user.role not in ['admin', 'teacher']:
        messages.error(request, 'You do not have permission to edit grades.')
        return redirect('grade_list')
    
    grade = get_object_or_404(Grade, pk=pk)
    
    if request.method == 'POST':
        form = GradeForm(request.POST, instance=grade)
        if form.is_valid():
            form.save()
            messages.success(request, 'Grade updated successfully!')
            return redirect('grade_list')
    else:
        form = GradeForm(instance=grade)
    
    return render(request, 'grades/edit.html', {'form': form, 'grade': grade})

@login_required
def delete_grade(request, pk):
    if request.user.role not in ['admin', 'teacher']:
        messages.error(request, 'You do not have permission to delete grades.')
        return redirect('grade_list')
    
    grade = get_object_or_404(Grade, pk=pk)
    if request.method == 'POST':
        grade.delete()
        messages.success(request, 'Grade deleted successfully!')
        return redirect('grade_list')
    
    return render(request, 'grades/confirm_delete.html', {'grade': grade})

@login_required
def view_grade(request, pk):
    grade = get_object_or_404(Grade, pk=pk)
    
    # Check permission
    if request.user.role == 'student':
        try:
            if grade.student.user != request.user:
                messages.error(request, 'You can only view your own grades.')
                return redirect('grade_list')
        except:
            pass
    
    return render(request, 'grades/view.html', {'grade': grade})