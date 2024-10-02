from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from .models import Task
from .serializers import TaskSerializer
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from .models import CUser
from .serializers import UserSerializer, UserCreateSerializer


class UserCreateView(generics.CreateAPIView):
    serializer_class = UserCreateSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):# cсоздание пользователя
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)  # Валидация данных
        self.perform_create(serializer)  # Сохранение нового пользователя
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            # Удаляем токен пользователя
            request.user.auth_token.delete()
            return Response(status=status.HTTP_200_OK)
        except Token.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class UserDetailView(generics.RetrieveUpdateAPIView):# детали о юзере
    queryset = CUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self): # Получение текущего аутентифицированного пользователя
        return self.request.user

    def patch(self, request, *args, **kwargs):
        user = self.get_object()
        print(f"Полученные данные для обновления: {request.data}")
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        print(f"Обновленный пользователь: {serializer.data}")  # Проверка обновленных данных
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        user.is_deleted = True  # Отмечаем пользователя как удаленного
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
########################################################################################################################

class TasksApiView(generics.ListAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer