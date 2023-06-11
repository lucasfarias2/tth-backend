from django.shortcuts import render
from rest_framework import generics
from .models import Goal, Objective, Task
from .serializers import GoalSerializer, ObjectiveSerializer, TaskSerializer

class GoalListCreateView(generics.ListCreateAPIView):
    queryset = Goal.objects.all()
    serializer_class = GoalSerializer

class ObjectiveListCreateView(generics.ListCreateAPIView):
    queryset = Objective.objects.all()
    serializer_class = ObjectiveSerializer

class TaskListCreateView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
