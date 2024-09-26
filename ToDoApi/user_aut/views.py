from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from .models import CustomUser
from .serializers import UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.filter(is_deleted=False)  # Исключаем удаленных пользователей
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.AllowAny()]  # Разрешаем доступ всем для создания пользователя
        return [permissions.IsAuthenticated()]

    def perform_destroy(self, instance):
        instance.is_deleted = True  # Мягкое удаление
        instance.save()

    # Дополнительные методы для входа, выхода и изменения пароля
    def login_user(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return Response({'status': 'logged in'}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

    def logout_user(self, request):
        logout(request)
        return Response({'status': 'logged out'}, status=status.HTTP_200_OK)

    def change_password(self, request):
        user = request.user
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        if user.check_password(old_password):
            user.set_password(new_password)
            user.save()
            return Response({'status': 'password updated'}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid old password'}, status=status.HTTP_400_BAD_REQUEST)

    def reset_password(self, request):
        # Реализуйте логику сброса пароля здесь
        pass