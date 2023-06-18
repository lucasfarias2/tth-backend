from datetime import date
from rest_framework.views import APIView
from django.contrib.auth import get_user_model, authenticate
from django.db.models import Sum
from django.http import Http404
from rest_framework import generics, status, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .auth import BearerTokenAuthentication
from .models import Goal, Objective, Habit, EffortLog
from .serializers import GoalSerializer, ObjectiveSerializer, HabitSerializer, EffortLogSerializer, UserSerializer

User = get_user_model()

class GoalListCreateView(generics.ListCreateAPIView):
    serializer_class = GoalSerializer
    authentication_classes = [BearerTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Goal.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class GoalRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = GoalSerializer
    authentication_classes = [BearerTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Goal.objects.filter(user=self.request.user)

class ObjectiveListCreateView(generics.ListCreateAPIView):
    serializer_class = ObjectiveSerializer
    authentication_classes = [BearerTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Objective.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ObjectiveRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ObjectiveSerializer
    authentication_classes = [BearerTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Objective.objects.filter(user=self.request.user)

class HabitListCreateView(generics.ListCreateAPIView):
    serializer_class = HabitSerializer
    authentication_classes = [BearerTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)

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
            "username": user.username,
            "email": user.email,
        }
        
        return Response(data)

class GoalWeeklyStatisticsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, week):
        goals = Goal.objects.filter(user=request.user)
        statistics = []

        for goal in goals:
            total_effort = EffortLog.objects.filter(habit__objective__goal=goal, week=week).aggregate(Sum('level')).get('level__sum', 0)
            total_points = EffortLog.objects.filter(habit__objective__goal=goal, week=week).aggregate(Sum('level')).get('level__sum', 0)

            if total_effort is None:
                total_effort = 0

            total_percentage = (total_effort / goal.total_effort_all_goals()) * 100 if goal.total_effort_all_goals() != 0 else 0.0

            statistics.append({
                'id': goal.id,
                'name': goal.name,
                'total_percentage': total_percentage,
                'total_points': total_points if total_points is not None else 0
            })

        total_effort_points = EffortLog.objects.filter(week=week).aggregate(Sum('level')).get('level__sum', 0)

        data = {
            'total_effort_points': total_effort_points if total_effort_points is not None else 0,
            'goals': statistics
        }

        return Response(data)

