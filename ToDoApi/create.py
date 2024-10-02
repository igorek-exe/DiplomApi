import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "your_project_name.settings")  # Замените на имя вашего проекта
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()
User.objects.create_superuser('god', 'admin@example.com', '123')
print("Суперпользователь 'admin' успешно создан.")