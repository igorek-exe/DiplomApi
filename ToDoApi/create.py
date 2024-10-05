import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ToDoApi.settings")  # Замените на имя вашего проекта
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()
# User.objects.create_superuser('god', 'admin@example.com', '123')
User.objects.create_user('user', 'user@example.com', 'aste11as')
User.objects.create_user('user1', 'user@example.com', 'aste11as')
User.objects.create_user('user2', 'user@example.com', 'aste11as')
print("пользователи успешно созданы.")