from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Task, Category, Priority
from .serializers import TaskSerializer, AdminUserSerializer, CategorySerializer, PrioritySerializer
from django.contrib.auth import get_user_model
from rest_framework import generics, viewsets
from .serializers import UserSerializer
from rest_framework import status
from djoser.views import UserViewSet
from django.utils import timezone

User = get_user_model()
#############################################USER##############################################

class UserListView(generics.ListAPIView):
    """Редактирование только админом поле is_staff and is_active(soft dellete by user)"""
    def get_serializer_class(self):
        if self.request.user.is_staff:
            return AdminUserSerializer  # Администратор получает доступ к расширенному сериализатору
        return UserSerializer  # Обычные пользователи получают ограниченный сериализатор

    def get_queryset(self):
        queryset = User.objects.all() if self.request.user.is_staff else User.objects.filter(is_active=True)
        user_id = self.kwargs.get('id')
        if user_id:
            queryset = queryset.filter(id=user_id)
        return queryset

class CustomUserViewSet(UserListView,UserViewSet):

    def retrieve(self, request, *args, **kwargs):
        """Получение данных пользователя по ID"""
        user_id = kwargs.get('id')
        user = self.get_queryset().filter(id=user_id).first()  # Получаем пользователя по ID из queryset
        if user:
            serializer = self.get_serializer(user)  # Получаем сериализатор
            return Response(serializer.data)
        return Response({"detail": "Пользователь не найден."}, status=status.HTTP_404_NOT_FOUND)

    def retrieve_me(self, request):
        """Получение данных текущего аутентифицированного пользователя"""
        user = request.user  # Получаем текущего пользователя из запроса
        serializer = self.get_serializer(user)  # Получаем сериализатор
        return Response(serializer.data)  # Возвращаем данные пользовател+


    def destroy(self, request, *args, **kwargs):

        if request.user.is_authenticated:
            target_user = self.get_object()

            if request.user.is_staff:
                # Полное удаление для администратора
                target_user.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)

            else:
                target_user.is_active = False
                target_user.save()
                return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(status=status.HTTP_403_FORBIDDEN)


    def update(self, request, *args, **kwargs):
        user = self.get_object()  # Получаем пользователя
        # Проверяем, является ли пользователь администратором
        if request.user.is_staff or request.user == user:
            if 'username' in request.data:
                user.username = request.data['username']
            serializer = self.get_serializer(user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        else:
            return Response({"detail": "У вас нет прав для изменения этого пользователя."},
                            status=status.HTTP_403_FORBIDDEN)

#############################################TASK##############################################

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
    def perform_create(self, serializer):
        # Автоматически установить пользователя, который создал задачу
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        # Реализуем soft delete
        instance.deleted = True
        instance.deleted_at = timezone.now()
        instance.save()

class PriorityViewSet(viewsets.ModelViewSet):
    queryset = Priority.objects.filter(deleted=False)
    serializer_class = PrioritySerializer
    permission_classes = [IsAuthenticated]
    def perform_create(self, serializer):
        # Автоматически установить пользователя, который создал задачу
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        # Реализуем soft delete
        instance.deleted = True
        instance.deleted_at = timezone.now()
        instance.save()

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.filter(deleted=False)
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Базовый запрос
        queryset = Task.objects.filter(deleted=False)
        # Если пользователь администратор, возвращаем все задачи
        if self.request.user.is_staff:
            queryset = Task.objects.all()

        # Фильтрация по статусу
        status = self.request.query_params.get('status')
        if status:
            queryset = queryset.filter(status=status)
        # Фильтрация по категории
        category_id = self.request.query_params.get('category')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        # Если пользователь не администратор, возвращаем только его задачи
        if not self.request.user.is_staff:
            queryset = queryset.filter(created_by=self.request.user)

        # Сортировка
        order_by = self.request.query_params.get('order_by', 'created_at')  # По умолчанию сортировка по дате создания
        order_direction = self.request.query_params.get('order_direction', 'asc')  # По умолчанию по возрастанию

        if order_direction == 'desc':
            queryset = queryset.order_by(f'-{order_by}')  # Убывающая сортировка
        else:
            queryset = queryset.order_by(order_by)  # Возрастающая сортировка

        return queryset
    def perform_create(self, serializer):
        # Автоматически установить пользователя, который создал задачу
        serializer.save(created_by=self.request.user)

    def perform_destroy(self, instance):
        # Реализуем soft delete
        instance.deleted = True
        instance.deleted_at = timezone.now()
        instance.save()