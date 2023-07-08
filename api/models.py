import datetime
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.conf import settings

class Habit(models.Model):
    name = models.CharField(max_length=255)
    starting_week = models.PositiveIntegerField(default=datetime.date.today().isocalendar()[1])
    expected_effort = models.IntegerField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    color = models.CharField(max_length=255, default="rose")
    year = models.PositiveIntegerField(default=datetime.date.today().year)

    def __str__(self):
        return f"{self.name} - From: week {self.starting_week}"

class Effort(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE)
    week = models.PositiveIntegerField(default=datetime.date.today().isocalendar()[1])
    level = models.IntegerField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    year = models.PositiveIntegerField(default=datetime.date.today().year)

    def __str__(self):
        return f"Habit: {self.habit.name} - Week: {self.week} - Level: {self.level}"

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)
    
class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.email} - {self.first_name} {self.last_name}"
    
class Ticket(models.Model):
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ]
    TYPE_CHOICES = [
        ('email', 'Email'),
        ('web', 'Web'),
    ]

    title = models.CharField(max_length=255)
    content = models.TextField(max_length=1000)
    sender = models.EmailField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='open')
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    creation_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title}"
    
class Announcement(models.Model):
    TYPE_CHOICES = [
        ('alert', 'Alert'),
        ('info', 'Info'),
        ('warning', 'Warning'),
    ]

    title = models.CharField(max_length=255)
    content = models.TextField(max_length=1000)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    starting_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"{self.title}"
