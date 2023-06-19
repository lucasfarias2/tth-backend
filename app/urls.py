from django.contrib import admin
from django.urls import path
from api.views import (
    HabitListCreateView, HabitRetrieveUpdateDestroyView, 
    RegisterView, LoginView, CurrentUserView, EffortLogListCreateView, 
    EffortLogRetrieveUpdateDestroyView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/register/', RegisterView.as_view(), name='register'),
    path('api/auth/login/', LoginView.as_view(), name='login'),
    path('api/auth/user/', CurrentUserView.as_view(), name='current-user'),
    path('api/habits/', HabitListCreateView.as_view(), name='habit-list-create'),
    path('api/habits/<int:pk>/', HabitRetrieveUpdateDestroyView.as_view(), name='habit-detail'),
    path('api/effortlogs/', EffortLogListCreateView.as_view(), name='effortlog-list-create'),
    path('api/effortlogs/<int:pk>/', EffortLogRetrieveUpdateDestroyView.as_view(), name='effortlog-detail'),
]
