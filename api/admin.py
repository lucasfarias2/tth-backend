from django.contrib import admin

from .models import Habit, Objective, Goal, EffortLog

admin.site.register(Habit)
admin.site.register(Objective)
admin.site.register(Goal)
admin.site.register(EffortLog)
