from .models import Task, CUser

from djoser.serializers import UserSerializer as BaseUserSerializer
from django.contrib.auth import update_session_auth_hash
from rest_framework import serializers


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = CUser
        fields = ['id', 'username', 'email', 'password']

    def create(self, validated_data):
        user = CUser(**validated_data)  # Создание нового экземпляра пользователя
        user.set_password(validated_data['password'])  # Хэширование пароля
        user.save()  # Сохранение пользователя в базе данных
        return user



class UserSerializer(BaseUserSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta(BaseUserSerializer.Meta):
        model = CUser
        fields = ['id', 'username', 'email', 'password',]

    def update(self, instance, validated_data): # Обновление имени пользователя
        if 'username' in validated_data:
            instance.username = validated_data['username']

        # Обновление пароля
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])
            update_session_auth_hash(self.context['request'], instance)  # Обновление сессии после изменения пароля

        instance.save()  # Сохраняем изменения
        return super().update(instance, validated_data)

#################################################################################################


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('title', 'description')