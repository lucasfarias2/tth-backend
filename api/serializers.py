from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Goal, Objective, Task

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

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
