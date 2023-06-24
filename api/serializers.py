from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Habit, Effort, CustomUser

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'password', 'first_name', 'last_name')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user

class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = '__all__'
        extra_kwargs = {'user': {'read_only': True}}

class EffortSerializer(serializers.ModelSerializer):
    habit = serializers.PrimaryKeyRelatedField(queryset=Habit.objects.all())

    class Meta:
        model = Effort
        fields = '__all__'
        extra_kwargs = {'user': {'read_only': True}}
    
    def to_representation(self, instance):
        self.fields['habit'] = HabitSerializer()
        return super(EffortSerializer, self).to_representation(instance)
