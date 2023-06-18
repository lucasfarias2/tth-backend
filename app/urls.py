from django.contrib import admin
from django.urls import path
from api.views import (
    GoalListCreateView, GoalDestroyView,
    ObjectiveListCreateView, ObjectiveDestroyView,
    TaskListCreateView, TaskDestroyView, RegisterView, LoginView, CurrentUserView
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/user/', CurrentUserView.as_view(), name='current-user'),
    path('api/goals/', GoalListCreateView.as_view(), name='goal-list-create'),
    path('api/goals/<int:pk>/', GoalDestroyView.as_view(), name='goal-destroy'),
    path('api/objectives/', ObjectiveListCreateView.as_view(), name='objective-list-create'),
    path('api/objectives/<int:pk>/', ObjectiveDestroyView.as_view(), name='objective-destroy'),
    path('api/tasks/', TaskListCreateView.as_view(), name='task-list-create'),
    path('api/tasks/<int:pk>/', TaskDestroyView.as_view(), name='task-destroy'),
]
