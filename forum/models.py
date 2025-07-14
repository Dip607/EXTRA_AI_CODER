from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class User(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('faculty', 'Faculty'),
    )
    DEPARTMENT_CHOICES = (
        ('CSE', 'CSE'),
        ('ECE', 'ECE'),
        ('ME', 'Mechanical'),
        ('CE', 'Civil'),
        ('EE', 'Electrical'),
    )
    YEAR_CHOICES = (
        (1, '1st Year'),
        (2, '2nd Year'),
        (3, '3rd Year'),
        (4, '4th Year'),
    )

    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    department = models.CharField(max_length=20, choices=DEPARTMENT_CHOICES)
    year = models.PositiveSmallIntegerField(choices=YEAR_CHOICES, null=True, blank=True)
    github_url = models.URLField(blank=True, null=True)
    is_verified_faculty = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.username} ({self.role})"


class Doubt(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    code_snippet = models.TextField(blank=True, null=True)
    ai_answer = models.TextField(blank=True, null=True)
    faculty_verified = models.BooleanField(default=False)
    faculty_suggestion = models.TextField(blank=True, null=True)  # ✅ New field
    created_at = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category, blank=True)
    is_public = models.BooleanField(default=True)
    verified_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='verified_doubts')

    def __str__(self):
        return self.title


# forum/models.py

class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"To {self.user.username}: {self.message[:30]}"

class Comment(models.Model):
    doubt = models.ForeignKey(Doubt, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.doubt.title}"
