from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Attendance
from students.models import Student
from courses.models import Course
from django.utils import timezone

@login_required
def attendance_list(request):
    # If user is a student, show only their attendance
    if request.user.role == 'student':
        try:
            student = Student.objects.get(user=request.user)
            attendances = Attendance.objects.filter(student=student)
        except Student.DoesNotExist:
            attendances = Attendance.objects.none()
    else:
        # Teachers and admins see all attendance
        attendances = Attendance.objects.all()
    
    return render(request, 'attendance/list.html', {'attendances': attendances})

@login_required
def mark_attendance(request):
    if request.method == 'POST':
        course_id = request.POST.get('course')
        date = request.POST.get('date')
        
        try:
            # For development, allow any user to mark attendance on any course
            course = Course.objects.get(id=course_id)
            # In production, add: , teacher=request.user
        except Course.DoesNotExist:
            messages.error(request, 'Invalid course selected.')
            return redirect('mark_attendance')
        
        # Get students enrolled in the course
        students = Student.objects.filter(courses=course)
        
        attendance_count = 0
        for student in students:
            status = request.POST.get(f'attendance_{student.id}')
            remarks = request.POST.get(f'remarks_{student.id}', '')
            
            if status:
                Attendance.objects.update_or_create(
                    student=student,
                    course=course,
                    date=date,
                    defaults={
                        'status': status,
                        'remarks': remarks,
                        'marked_by': request.user
                    }
                )
                attendance_count += 1
        
        messages.success(request, f'Attendance marked for {attendance_count} students!')
        return redirect('attendance_list')
    
    # Show all courses for easier testing (in production, filter by teacher)
    courses = Course.objects.all()
    students = Student.objects.all()
    today = timezone.now().date()
    return render(request, 'attendance/mark.html', {
        'courses': courses,
        'students': students,
        'today': today
    })