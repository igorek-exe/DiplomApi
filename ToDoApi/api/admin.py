
from django.contrib import admin
from .models import CUser, Category, Priority, Task

# Регистрация модели в админке
admin.site.register(CUser)
admin.site.register(Task)
admin.site.register(Priority)
admin.site.register(Category)

