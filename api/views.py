import datetime
from rest_framework.views import APIView
from django.contrib.auth import get_user_model, authenticate
from django.db.models import F, Q, Sum
from rest_framework import generics, status, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .auth import BearerTokenAuthentication
from .models import Habit, Effort
from .serializers import HabitSerializer, EffortSerializer, UserSerializer

User = get_user_model()

class HabitListCreateView(generics.ListCreateAPIView):
    serializer_class = HabitSerializer
    authentication_classes = [BearerTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        year = self.request.query_params.get('year', datetime.date.today().year)
        week = self.request.query_params.get('week', None)
        
        query = Q(year=year) & Q(user=self.request.user)

        if week is not None:
            week = int(week)
            query &= Q(starting_week__lte=week)

        return Habit.objects.filter(query).order_by('starting_week', F('expected_effort').desc())

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class HabitRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = HabitSerializer
    authentication_classes = [BearerTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)
    
class EffortListCreateView(generics.ListCreateAPIView):
    serializer_class = EffortSerializer
    authentication_classes = [BearerTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        year = self.request.query_params.get('year', datetime.date.today().year)
        return Effort.objects.filter(Q(year=year) & Q(user=self.request.user))

    def create(self, request, *args, **kwargs):
        habit = request.data.get('habit')
        week = request.data.get('week')

        if Effort.objects.filter(habit=habit, week=week, user=request.user).exists():
            raise ValidationError("Effort already set for that week and habit.")

        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class EffortRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = EffortSerializer
    authentication_classes = [BearerTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Effort.objects.filter(user=self.request.user)

class EffortListByWeekView(generics.ListAPIView):
    serializer_class = EffortSerializer
    authentication_classes = [BearerTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        week = self.kwargs['week']
        year = self.request.query_params.get('year', datetime.date.today().year)
        return Effort.objects.filter(Q(week=week) & Q(year=year) & Q(user=self.request.user))

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        token, _ = Token.objects.get_or_create(user=User.objects.get(email=request.data['email']))
        response.data['token'] = token.key
        response.data['first_name'] = request.data['first_name']
        response.data['last_name'] = request.data['last_name']
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

class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=204)

class EffortCompletionView(APIView):
    authentication_classes = [BearerTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        week = self.kwargs['week']
        user = request.user

        # Get the total expected effort for the week
        total_expected_effort = Habit.objects.filter(user=user, starting_week__lte=week).aggregate(Sum('expected_effort'))['expected_effort__sum'] or 0

        # Get the total actual effort for the week
        total_actual_effort = Effort.objects.filter(user=user, week=week).aggregate(Sum('level'))['level__sum'] or 0

        # Calculate the completion percentage
        if total_expected_effort > 0:
            completion_percentage = (total_actual_effort / total_expected_effort) * 100
        else:
            completion_percentage = 0

        return Response({'completion_percentage': completion_percentage})

class HabitPerformanceView(generics.ListAPIView):
    serializer_class = EffortSerializer
    authentication_classes = [BearerTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        habit_id = self.kwargs['habit_id']
        return Effort.objects.filter(habit_id=habit_id, user=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        habit = Habit.objects.get(id=self.kwargs['habit_id'], user=request.user)

        performance_data = []
        total_performance_percentage = 0
        for effort in queryset:
            expected_effort = habit.expected_effort
            actual_effort = effort.level

            # Calculate the performance percentage for the week
            if expected_effort > 0:
                performance_percentage = (actual_effort / expected_effort) * 100
            else:
                performance_percentage = 0

            total_performance_percentage += performance_percentage

            performance_data.append({
                'week': effort.week,
                'performance_percentage': performance_percentage
            })

        if queryset.count() > 0:
            average_performance_percentage = total_performance_percentage / queryset.count()
        else:
            average_performance_percentage = 0

        return Response({
            'performance_data': performance_data, 
            'average_performance_percentage': average_performance_percentage
        })

class YearlyHabitPerformanceView(APIView):
    authentication_classes = [BearerTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        current_week = datetime.date.today().isocalendar()[1]
        current_year = datetime.date.today().year
        habits = Habit.objects.filter(user=request.user, year=current_year)

        response = []
        
        for habit in habits:
            total_expected_effort = 0
            total_effort = 0
            
            for week in range(1, current_week + 1):
                expected_effort = habit.expected_effort if week >= habit.starting_week else 0
                total_expected_effort += expected_effort

                try:
                    effort = Effort.objects.get(habit=habit, week=week, year=current_year, user=request.user)
                    total_effort += effort.level
                except Effort.DoesNotExist:
                    pass
                
            if total_expected_effort > 0:
                performance_percentage = (total_effort / total_expected_effort) * 100
            else:
                performance_percentage = 0

            response.append({
                "habit": habit.name,
                "performance_percentage": performance_percentage
            })
        
        return Response(response)
