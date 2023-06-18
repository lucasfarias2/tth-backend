from django.contrib import admin
from django.urls import path
from api.views import (
    GoalListCreateView, ObjectiveListCreateView, HabitListCreateView, 
    GoalRetrieveUpdateDestroyView, ObjectiveRetrieveUpdateDestroyView, HabitRetrieveUpdateDestroyView,
    RegisterView, LoginView, CurrentUserView, EffortLogListCreateView, EffortLogRetrieveUpdateDestroyView
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/user/', CurrentUserView.as_view(), name='current-user'),
    path('api/goals/', GoalListCreateView.as_view(), name='goal-list-create'),
    path('api/goals/<int:pk>/', GoalRetrieveUpdateDestroyView.as_view(), name='goal-detail'),
    path('api/objectives/', ObjectiveListCreateView.as_view(), name='objective-list-create'),
    path('api/objectives/<int:pk>/', ObjectiveRetrieveUpdateDestroyView.as_view(), name='objective-detail'),
    path('api/habits/', HabitListCreateView.as_view(), name='habit-list-create'),
    path('api/habits/<int:pk>/', HabitRetrieveUpdateDestroyView.as_view(), name='habit-detail'),
    path('api/effortlogs/', EffortLogListCreateView.as_view(), name='effortlog-list-create'),
    path('api/effortlogs/<int:pk>/', EffortLogRetrieveUpdateDestroyView.as_view(), name='effortlog-detail'),
]
