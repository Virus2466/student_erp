from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegistrationForm, UserProfileForm
from students.models import Student
from courses.models import Course
from grades.models import Grade

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('dashboard')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def dashboard(request):
    context = {}
    
    if request.user.role == 'student':
        try:
            student = Student.objects.get(user=request.user)
            courses = student.courses.all()
            recent_grades = Grade.objects.filter(student=student)[:10]
            
            context.update({
                'student': student,
                'courses': courses,
                'recent_grades': recent_grades,
                'total_courses': courses.count(),
                'gpa': calculate_gpa(student),
            })
        except Student.DoesNotExist:
            pass
    
    elif request.user.role == 'teacher':
        courses = Course.objects.filter(teacher=request.user)
        total_students = sum(course.students.count() for course in courses)
        context.update({
            'courses': courses,
            'total_courses': courses.count(),
            'total_students': total_students,
        })
    
    return render(request, 'accounts/dashboard.html', context)

def calculate_gpa(student):
    grades = Grade.objects.filter(student=student)
    if grades.exists():
        grade_points = {'A': 4.0, 'B': 3.0, 'C': 2.0, 'D': 1.0, 'F': 0}
        total_points = sum(grade_points[g.grade] for g in grades)
        return round(total_points / grades.count(), 2)
    return 0

@login_required
def profile(request):
    return render(request, 'accounts/profile.html', {'user': request.user})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'accounts/edit_profile.html', {'form': form})