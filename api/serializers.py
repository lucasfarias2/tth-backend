from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Habit, Effort, CustomUser, Ticket, Announcement

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ('email', 'old_password', 'password', 'first_name', 'last_name')

    def validate(self, attrs):
        user = self.instance
        old_password = attrs.get('old_password')
        
        if not user.check_password(old_password):
            raise serializers.ValidationError("Old password is not correct")
        
        return attrs

    def create(self, validated_data):
        user = CustomUser(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        old_password = validated_data.pop('old_password', None)
        user = super().update(instance, validated_data)

        if password and old_password:
            user.set_password(password)
            user.save()

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

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'first_name', 'last_name']  # Include any other fields you want

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        return user

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'

class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = '__all__'

class UserListSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = '__all__'
