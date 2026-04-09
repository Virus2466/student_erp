from django.core.management.base import BaseCommand
from django.utils import timezone
from accounts.models import User
from students.models import Student
from courses.models import Course
from attendance.models import Attendance
from datetime import timedelta

class Command(BaseCommand):
    help = 'Populate the database with dummy courses, students, and teachers'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting to populate database...'))
        
        # Create Teachers
        teachers_data = [
            {'username': 'teacher1', 'email': 'teacher1@college.com', 'first_name': 'Dr.', 'last_name': 'Kapoor'},
            {'username': 'teacher2', 'email': 'teacher2@college.com', 'first_name': 'Prof.', 'last_name': 'Iyer'},
            {'username': 'teacher3', 'email': 'teacher3@college.com', 'first_name': 'Dr.', 'last_name': 'Reddy'},
        ]
        
        teachers = []
        for teacher_data in teachers_data:
            teacher, created = User.objects.get_or_create(
                username=teacher_data['username'],
                defaults={
                    'email': teacher_data['email'],
                    'first_name': teacher_data['first_name'],
                    'last_name': teacher_data['last_name'],
                    'role': 'teacher',
                    'is_active': True,
                }
            )
            if created:
                teacher.set_password('password123')
                teacher.save()
                self.stdout.write(self.style.SUCCESS(f'Created teacher: {teacher.username}'))
            teachers.append(teacher)
        
        # Create Courses
        courses_data = [
            {'code': 'CS101', 'name': 'Introduction to Programming', 'credits': 3, 'department': 'Computer Science', 'teacher': teachers[0]},
            {'code': 'CS201', 'name': 'Data Structures', 'credits': 3, 'department': 'Computer Science', 'teacher': teachers[0]},
            {'code': 'CS301', 'name': 'Web Development', 'credits': 4, 'department': 'Computer Science', 'teacher': teachers[1]},
            {'code': 'MATH101', 'name': 'Calculus I', 'credits': 4, 'department': 'Mathematics', 'teacher': teachers[1]},
            {'code': 'MATH201', 'name': 'Linear Algebra', 'credits': 3, 'department': 'Mathematics', 'teacher': teachers[2]},
            {'code': 'ENG101', 'name': 'English Composition', 'credits': 3, 'department': 'English', 'teacher': teachers[2]},
        ]
        
        courses = []
        for course_data in courses_data:
            course, created = Course.objects.get_or_create(
                code=course_data['code'],
                defaults={
                    'name': course_data['name'],
                    'credits': course_data['credits'],
                    'department': course_data['department'],
                    'teacher': course_data['teacher'],
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created course: {course.code}'))
            courses.append(course)
        
        # Create Students
        students_data = [
            {'username': 'student1', 'email': 'student1@college.com', 'first_name': 'Aarav', 'last_name': 'Sharma', 'student_id': 'STU001'},
            {'username': 'student2', 'email': 'student2@college.com', 'first_name': 'Priya', 'last_name': 'Patel', 'student_id': 'STU002'},
            {'username': 'student3', 'email': 'student3@college.com', 'first_name': 'Rohan', 'last_name': 'Gupta', 'student_id': 'STU003'},
            {'username': 'student4', 'email': 'student4@college.com', 'first_name': 'Ananya', 'last_name': 'Singh', 'student_id': 'STU004'},
            {'username': 'student5', 'email': 'student5@college.com', 'first_name': 'Arjun', 'last_name': 'Kumar', 'student_id': 'STU005'},
            {'username': 'student6', 'email': 'student6@college.com', 'first_name': 'Neha', 'last_name': 'Desai', 'student_id': 'STU006'},
            {'username': 'student7', 'email': 'student7@college.com', 'first_name': 'Vikram', 'last_name': 'Rao', 'student_id': 'STU007'},
            {'username': 'student8', 'email': 'student8@college.com', 'first_name': 'Divya', 'last_name': 'Nambiar', 'student_id': 'STU008'},
        ]
        
        student_objects = []
        for student_data in students_data:
            user, created = User.objects.get_or_create(
                username=student_data['username'],
                defaults={
                    'email': student_data['email'],
                    'first_name': student_data['first_name'],
                    'last_name': student_data['last_name'],
                    'role': 'student',
                    'is_active': True,
                }
            )
            if created:
                user.set_password('password123')
                user.save()
                self.stdout.write(self.style.SUCCESS(f'Created student user: {user.username}'))
            
            student, created = Student.objects.get_or_create(
                user=user,
                defaults={
                    'student_id': student_data['student_id'],
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created student profile: {student.student_id}'))
            
            student_objects.append(student)
        
        # Assign students to courses
        for i, student in enumerate(student_objects):
            # Each student gets 3-4 courses
            assigned_courses = courses[i % len(courses):(i % len(courses)) + 3]
            for course in assigned_courses:
                student.courses.add(course)
            self.stdout.write(self.style.SUCCESS(f'Assigned courses to {student.user.username}'))
        
        # Create some sample attendance records for the last 5 days
        status_choices = ['present', 'absent', 'late', 'excused']
        today = timezone.now().date()
        
        for i in range(5):
            attendance_date = today - timedelta(days=5-i)
            for student in student_objects:
                for course in student.courses.all():
                    status = status_choices[i % len(status_choices)]
                    Attendance.objects.get_or_create(
                        student=student,
                        course=course,
                        date=attendance_date,
                        defaults={
                            'status': status,
                            'remarks': 'Sample attendance record' if status == 'late' else '',
                            'marked_by': course.teacher,
                        }
                    )
        
        self.stdout.write(self.style.SUCCESS(self.style.HTTP_SUCCESS('✓ Database populated successfully!')))
        self.stdout.write(self.style.HTTP_INFO('\nYou can now login with:'))
        self.stdout.write(self.style.HTTP_INFO('Teachers: teacher1, teacher2, teacher3'))
        self.stdout.write(self.style.HTTP_INFO('Students: student1-student8'))
        self.stdout.write(self.style.HTTP_INFO('Password for all: password123'))
