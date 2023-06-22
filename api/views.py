from rest_framework.views import APIView
from django.contrib.auth import get_user_model, authenticate
from django.db.models import F
from rest_framework import generics, status, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .auth import BearerTokenAuthentication
from .models import Habit, EffortLog
from .serializers import HabitSerializer, EffortLogSerializer, UserSerializer

User = get_user_model()

class HabitListCreateView(generics.ListCreateAPIView):
    serializer_class = HabitSerializer
    authentication_classes = [BearerTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user).order_by('starting_week', F('expected_effort').desc())

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class HabitRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = HabitSerializer
    authentication_classes = [BearerTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)
    
class EffortLogListCreateView(generics.ListCreateAPIView):
    serializer_class = EffortLogSerializer
    authentication_classes = [BearerTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return EffortLog.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        habit = request.data.get('habit')
        week = request.data.get('week')

        if EffortLog.objects.filter(habit=habit, week=week, user=request.user).exists():
            raise ValidationError("Effort already set for that week and habit.")

        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class EffortLogRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = EffortLogSerializer
    authentication_classes = [BearerTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return EffortLog.objects.filter(user=self.request.user)

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        token, _ = Token.objects.get_or_create(user=User.objects.get(username=request.data['username']))
        response.data['token'] = token.key
        return response

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(email=email, password=password)

        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"token": token.key})
        
        return Response({"error": "Wrong Credentials"}, status=status.HTTP_400_BAD_REQUEST)

class CurrentUserView(APIView):
    authentication_classes = [BearerTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        data = {
            "id": user.id,
            "email": user.email,
            "is_staff": user.is_staff,
            "is_superuser": user.is_superuser,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "date_joined": user.date_joined,
            "last_login": user.last_login,
        }
        
        return Response(data)
