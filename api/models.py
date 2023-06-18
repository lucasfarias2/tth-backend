import datetime
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
        return f"{self.name}"

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
        return f"{self.name}"

class Habit(models.Model):
    name = models.CharField(max_length=255)
    objective = models.ForeignKey("Objective", on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}"

class EffortLog(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE)
    week = models.PositiveIntegerField(default=datetime.date.today().isocalendar()[1])
    level = models.IntegerField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"Habit: {self.habit.name} - Week: {self.week} - Level: {self.level}"
