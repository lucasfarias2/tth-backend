import datetime
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.conf import settings

class Goal(models.Model):
    COLOR_CHOICES = (
        ("blue", "Blue"),
        ("red", "Red"),
        ("green", "Green"),
        ("yellow", "Yellow"),
        ("purple", "Purple"),
        ("orange", "Orange"),
        ("pink", "Pink"),
        ("gray", "Gray"),
        ("brown", "Brown"),
        ("black", "Black"),
    )

    name = models.CharField(max_length=255)
    year = models.PositiveIntegerField()
    color = models.CharField(max_length=50, choices=COLOR_CHOICES, default='indianred')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.year}"

    def total_effort_all_goals(self):
        total_effort = EffortLog.objects.filter(habit__objective__goal__year=self.year, habit__user=self.user).aggregate(models.Sum('level')).get('level__sum')
        return total_effort if total_effort is not None else 0

class Objective(models.Model):
    QUARTER_CHOICES = (
        ("Q1", "Q1"),
        ("Q2", "Q2"),
        ("Q3", "Q3"),
        ("Q4", "Q4"),
    )

    name = models.CharField(max_length=255)
    goal = models.ForeignKey("Goal", on_delete=models.CASCADE)
    quarter = models.CharField(max_length=2, choices=QUARTER_CHOICES)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.quarter} - {self.goal.name} - {self.goal.year}"

class Habit(models.Model):
    name = models.CharField(max_length=255)
    objective = models.ForeignKey("Objective", on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.objective.name} - {self.objective.quarter} - {self.objective.goal.name} - {self.objective.goal.year}"

class EffortLog(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE)
    week = models.PositiveIntegerField(default=datetime.date.today().isocalendar()[1])
    level = models.IntegerField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

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
        return self.email
    
