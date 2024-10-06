from django.contrib.auth import get_user_model
from .models import Task, Category, Priority
from rest_framework import serializers
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer, UserSerializer as BaseUserSerializer


User = get_user_model()

class UserCreateSerializer(BaseUserCreateSerializer):
    email = serializers.EmailField(required=True)
    class Meta(BaseUserCreateSerializer.Meta):
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data): # Проверка уникальности email
        if User.objects.filter(email=validated_data['email']).exists():
            raise serializers.ValidationError({"email": "Этот адрес электронной почты уже занят."})

        user = User(**validated_data)
        user.set_password(validated_data['password'])  # Хэшируем пароль
        user.save()
        return user

class UserSerializer(BaseUserSerializer):
    email = serializers.EmailField(required=True)
    class Meta(BaseUserSerializer.Meta):
        model = User
        fields = ['id', 'username', 'email']

class AdminUserSerializer(BaseUserSerializer):
    email = serializers.EmailField(required=True)
    class Meta(BaseUserSerializer.Meta):
        model = User
        fields = ['id', 'username', 'email', 'is_active', 'is_staff']  # Поля для администратора


#########################################################TASKS############################


class TaskSerializer(serializers.ModelSerializer):
    created_by = serializers.SerializerMethodField()
    class Meta:
        model = Task
        fields = ['id','created_by', 'title', 'description',
                  'status', 'category', 'priority', 'completed',
                  'created_at', 'updated_at',"deleted_at", "deleted"]
        read_only_fields = ['created_by', 'created_at', 'updated_at', "deleted_at", "deleted"]
    @staticmethod
    def get_created_by(obj):
        return obj.created_by.username if obj.created_by else None

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'created_at',
                  'updated_at', 'deleted_at', 'deleted',]
        read_only_fields =['id', 'created_at', 'updated_at', 'deleted_at', 'deleted']


class PrioritySerializer(serializers.ModelSerializer):
    class Meta:
        model = Priority
        fields = ['id', 'name', 'created_at', 'updated_at', 'deleted_at', 'deleted']
        read_only_fields = ['id', 'created_at', 'updated_at', 'deleted_at', 'deleted']

