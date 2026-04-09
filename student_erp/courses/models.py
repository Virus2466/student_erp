from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Course(models.Model):
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=200)
    credits = models.IntegerField()
    department = models.CharField(max_length=100)
    teacher = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, limit_choices_to={'role': 'teacher'})
    
    def __str__(self):
        return f"{self.code} - {self.name}"