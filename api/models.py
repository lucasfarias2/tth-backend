from django.db import models
import datetime


class Task(models.Model):
    STATUS_CHOICES = (
        ("todo", "To Do"),
        ("completed", "Completed"),
    )

    name = models.CharField(max_length=255)
    week = models.PositiveIntegerField(default=datetime.date.today().isocalendar()[1])
    objective = models.ForeignKey("Objective", on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="todo")

    def __str__(self):
        return self.name


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

    def __str__(self):
        return self.name


class Goal(models.Model):
    name = models.CharField(max_length=255)
    year = models.PositiveIntegerField()

    def __str__(self):
        return self.name
