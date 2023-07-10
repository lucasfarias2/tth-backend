import datetime
from rest_framework.views import APIView
from django.contrib.auth import get_user_model, authenticate
from django.db.models import F, Q, Sum
from rest_framework import generics, status, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import PageNumberPagination
from .auth import BearerTokenAuthentication
from .models import Habit, Effort, Ticket, Announcement, Feature
from .serializers import (HabitSerializer, EffortSerializer, UserSerializer,
                          UserRegistrationSerializer, TicketSerializer, AnnouncementSerializer, UserListSerializer, FeatureSerializer)

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
    serializer_class = UserRegistrationSerializer
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

        habits = Habit.objects.filter(user=user,
                                        starting_week__lte=week,
                                        ending_week__gte=week # Habits that ended during or after the requested week
                                    )

        total_percentage = 0

        for habit in habits:
            expected_effort = habit.expected_effort

            # Get the total actual effort for the week for this habit
            total_actual_effort = Effort.objects.filter(user=user, week=week, habit=habit).aggregate(Sum('level'))['level__sum'] or 0

            # Calculate the completion percentage for this habit
            if total_actual_effort >= expected_effort:
                completion_percentage = 100
            else:
                completion_percentage = (total_actual_effort / expected_effort) * 100

            total_percentage += completion_percentage

        # Calculate the average completion percentage
        if habits:
            average_completion_percentage = total_percentage / len(habits)
        else:
            average_completion_percentage = 0

        return Response({'completion_percentage': average_completion_percentage})


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
                'performance_percentage': round(performance_percentage, 2)
            })

        if queryset.count() > 0:
            average_performance_percentage = total_performance_percentage / queryset.count()
        else:
            average_performance_percentage = 0

        return Response({
            'performance_data': performance_data, 
            'average_performance_percentage': round(average_performance_percentage, 2)
        })

class YearlyHabitPerformanceView(generics.ListAPIView):
    serializer_class = HabitSerializer
    authentication_classes = [BearerTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        current_week = datetime.date.today().isocalendar()[1]
        habits = Habit.objects.filter(user=self.request.user, starting_week__lte=current_week)
        habit_performance = []

        total_effort_points = 0
        for habit in habits:
            effort_points = Effort.objects.filter(habit=habit, week__lte=current_week).aggregate(Sum('level'))['level__sum'] or 0
            total_effort_points += effort_points

        for habit in habits:
            habit_effort_points = Effort.objects.filter(habit=habit, week__lte=current_week).aggregate(Sum('level'))['level__sum'] or 0
            weeks_since_start = current_week - habit.starting_week + 1
            performance_percentage = 0
            if habit.expected_effort > 0:
                performance_percentage = (habit_effort_points / (habit.expected_effort * weeks_since_start)) * 100
            contribution_percentage = 0
            if total_effort_points > 0:
                contribution_percentage = (habit_effort_points / total_effort_points) * 100

            habit_performance.append({
                'habit': HabitSerializer(habit).data,
                'performance_percentage': round(performance_percentage, 2),
                'contribution_percentage': round(contribution_percentage, 2),
            })

        # Sort the habit_performance list by contribution_percentage in descending order
        habit_performance = sorted(habit_performance, key=lambda k: k['contribution_percentage'], reverse=True)

        return Response(habit_performance)
    
class RecentCompletionsView(APIView):
    authentication_classes = [BearerTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_completion_percentage(self, user, week):
        # Get the total expected effort for the week
        total_expected_effort = Habit.objects.filter(user=user, starting_week__lte=week).aggregate(Sum('expected_effort'))['expected_effort__sum'] or 0

        # Get the total actual effort for the week
        total_actual_effort = Effort.objects.filter(user=user, week=week).aggregate(Sum('level'))['level__sum'] or 0

        # Calculate the completion percentage
        if total_expected_effort > 0:
            return round((total_actual_effort / total_expected_effort) * 100, 2)
        else:
            return 0

    def get(self, request, *args, **kwargs):
        user = request.user
        current_week = datetime.date.today().isocalendar()[1]

        response = []

        # Calculate completion percentages and differences for the current week and the 4 previous weeks
        for i, week in enumerate(range(current_week - 4, current_week + 1)):
            completion_percentage = self.get_completion_percentage(user, week)

            if i > 0:
                difference = round(completion_percentage - response[i - 1]['completion_percentage'], 2)
            else:
                difference = 0

            response.append({
                'week': week,
                'completion_percentage': completion_percentage,
                'difference': difference,
            })

        return Response(response)

class SiteConfigView(APIView):
    """
    API endpoint that returns site-wide configuration data
    """

    def get(self, request, format=None):
        # You can get the current week number using datetime.date.today().isocalendar()[1]
        current_week = datetime.date.today().isocalendar()[1]

        # Later, you can add more global variables here
        data = {
            "current_week": current_week,
        }

        return Response(data)

class UserUpdateView(generics.UpdateAPIView):
    serializer_class = UserSerializer
    authentication_classes = [BearerTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

class UserListView(generics.ListAPIView):
    serializer_class = UserListSerializer
    permission_classes = [permissions.IsAdminUser]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        queryset = User.objects.all().order_by('-date_joined')
        email = self.request.query_params.get('email')
        sort = self.request.query_params.get('sort')

        if email:
            queryset = queryset.filter(email__icontains=email)

        if sort == 'creation_date':
            queryset = queryset.order_by('date_joined')

        return queryset

class TicketListCreateView(generics.ListCreateAPIView):
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        return Ticket.objects.order_by('-creation_date')
   
# required of normal users
class TicketCreateView(generics.CreateAPIView):
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user.email)

class TicketRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = Ticket.objects.all()

class AnnouncementListCreateView(generics.ListCreateAPIView):
    serializer_class = AnnouncementSerializer
    permission_classes = [permissions.IsAdminUser]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        return Announcement.objects.all()

class AnnouncementRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AnnouncementSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = Announcement.objects.all()

class FeatureListCreateView(generics.ListCreateAPIView):
    serializer_class = FeatureSerializer
    permission_classes = [permissions.IsAdminUser]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        return Feature.objects.all()

class FeatureRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = FeatureSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = Feature.objects.all()

class UserTicketListView(generics.ListAPIView):
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAuthenticated]  # Ensures only authenticated users can access this view

    def get_queryset(self):
        """
        This view should return a list of all the tickets
        for the currently authenticated user.
        """
        user = self.request.user
        return Ticket.objects.filter(sender=user.email)
    

class PublicFeatureListView(generics.ListAPIView):
    serializer_class = FeatureSerializer

    def get_queryset(self):
        return Feature.objects
