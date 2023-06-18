from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Goal, Objective, Habit, EffortLog, CustomUser

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user


class GoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = '__all__'
        extra_kwargs = {'user': {'read_only': True}}

class ObjectiveSerializer(serializers.ModelSerializer):
    goal = serializers.PrimaryKeyRelatedField(queryset=Goal.objects.all())

    class Meta:
        model = Objective
        fields = '__all__'
        extra_kwargs = {'user': {'read_only': True}}

    def to_representation(self, instance):
        self.fields['goal'] = GoalSerializer()
        return super(ObjectiveSerializer, self).to_representation(instance)

class HabitSerializer(serializers.ModelSerializer):
    objective = serializers.PrimaryKeyRelatedField(queryset=Objective.objects.all())
    
    class Meta:
        model = Habit
        fields = '__all__'
        extra_kwargs = {'user': {'read_only': True}}
    
    def to_representation(self, instance):
        self.fields['objective'] = ObjectiveSerializer()
        return super(HabitSerializer, self).to_representation(instance)

class EffortLogSerializer(serializers.ModelSerializer):
    habit = serializers.PrimaryKeyRelatedField(queryset=Habit.objects.all())

    class Meta:
        model = EffortLog
        fields = '__all__'
        extra_kwargs = {'user': {'read_only': True}}
    
    def to_representation(self, instance):
        self.fields['habit'] = HabitSerializer()
        return super(EffortLogSerializer, self).to_representation(instance)
