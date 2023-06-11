from rest_framework import serializers
from .models import Goal, Objective, Task

class GoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = '__all__'

class ObjectiveSerializer(serializers.ModelSerializer):
    goal = GoalSerializer()  # Include the GoalSerializer nested within the ObjectiveSerializer

    class Meta:
        model = Objective
        fields = '__all__'

class TaskSerializer(serializers.ModelSerializer):
    objective = ObjectiveSerializer()  # Include the ObjectiveSerializer nested within the TaskSerializer
    
    class Meta:
        model = Task
        fields = '__all__'
