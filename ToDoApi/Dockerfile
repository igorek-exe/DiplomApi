# Используем официальный образ Python
FROM python:3.12-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем requirements.txt и устанавливаем зависимости
COPY requirements.txt ./
# Копируем все файлы проекта в контейнер
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
# Открываем порт 8000

EXPOSE 8000

# Запускаем приложение
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
