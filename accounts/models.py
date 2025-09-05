from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ("student", "Student"),
        ("teacher", "Teacher"),
        ("admin", "Admin"),
        ("super admin", "Superadmin")
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.username} ({self.role})"

class BaseProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.__class__.__name__}: {self.user.username}"


class StudentProfile(BaseProfile):
    roll = models.CharField(max_length=20, unique=True)
    course = models.CharField(max_length=100)
    year = models.IntegerField()
    section = models.CharField(max_length=10)


class TeacherProfile(BaseProfile):
    subject = models.CharField(max_length=50)
    department = models.CharField(max_length=100)
    designation = models.CharField(max_length=50)


class AdminProfile(BaseProfile):
    office = models.CharField(max_length=50)
    position = models.CharField(max_length=50)