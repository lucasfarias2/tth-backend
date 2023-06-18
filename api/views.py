from django.contrib.auth import get_user_model, authenticate
from rest_framework import generics, status, permissions
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Goal, Objective, Task
from .serializers import GoalSerializer, ObjectiveSerializer, TaskSerializer, UserSerializer

class GoalListCreateView(generics.ListCreateAPIView):
    queryset = Goal.objects.all()
    serializer_class = GoalSerializer

class GoalDestroyView(generics.DestroyAPIView):
    queryset = Goal.objects.all()
    serializer_class = GoalSerializer

class ObjectiveListCreateView(generics.ListCreateAPIView):
    queryset = Objective.objects.all()
    serializer_class = ObjectiveSerializer

class ObjectiveDestroyView(generics.DestroyAPIView):
    queryset = Objective.objects.all()
    serializer_class = ObjectiveSerializer

class TaskListCreateView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

class TaskDestroyView(generics.DestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

User = get_user_model()

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
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"token": token.key})
        else:
            return Response({"error": "Wrong Credentials"}, status=status.HTTP_400_BAD_REQUEST)

class CurrentUserView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        token_key = request.headers.get('Authorization').split(' ')[1]
        token = Token.objects.get(key=token_key)
        user = User.objects.get(id=token.user_id)

        data = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
        }
        return Response(data)
