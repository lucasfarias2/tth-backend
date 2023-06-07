from django.contrib import admin

from .models import Task, Objective, Goal

admin.site.register(Task)

admin.site.register(Objective)

admin.site.register(Goal)
