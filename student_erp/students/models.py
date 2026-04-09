from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    student_id = models.CharField(max_length=20, unique=True)
    courses = models.ManyToManyField('courses.Course', related_name='students')
    
    def __str__(self):
        return f"{self.user.get_full_name()} ({self.student_id})"