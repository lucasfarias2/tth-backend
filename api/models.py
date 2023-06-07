from django.db import models

class Task(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Objective(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Goal(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
