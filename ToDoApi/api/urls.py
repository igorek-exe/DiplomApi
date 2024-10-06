from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views import UserListView, CustomUserViewSet,CategoryViewSet, PriorityViewSet, TaskViewSet

router = DefaultRouter()

router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'priorities', PriorityViewSet, basename='priority')
router.register(r'tasks', TaskViewSet, basename='tasks')

urlpatterns = [
    path('users/me/', CustomUserViewSet.as_view({'get': 'retrieve_me',}), name='user-me'),
    path('users/<int:id>/', CustomUserViewSet.as_view({
                                                        'get':'retrieve',
                                                        'put': 'update',
                                                        'patch': 'partial_update',
                                                        'delete': 'destroy',
                                                       }),
         name='user-manage'),

    path('all_users/', UserListView.as_view(), name='cuser-list'),# Все юзеры
    path('', include('djoser.urls')),  # для аутентификации
    path('', include('djoser.urls.authtoken')),

]
urlpatterns += router.urls
# http://127.0.0.1:8000/api/token/login/ получение токена
# /api/token/logout/ удаление токена
#/api/users/set_password/ изменить пароль юзера
# {
#     "current_password": "your_current_password",
#     "new_password": "your_new_password"
# }
#/api/users/reset_password/ сбросить пароль юзера
# приходит в консоль ссылка
# /api/users/reset_password_confirm/
# {
#     "new_password": "your_new_password_here",
#     "uid": "MTk",  // ваш закодированный uid
#     "token": "ceea5y-242c6f5c97e5ceff179b0134fcf752fe"  // ваш токен
# }

# GET	/tasks/	Получить список всех задач	list
# POST	/tasks/	Создать новую задачу	create
# GET	/tasks/{id}/	Получить задачу по ID	retrieve
# PUT	/tasks/{id}/	Обновить всю задачу по ID	update
# PATCH	/tasks/{id}/	Частичное обновление задачи	partial_update
# DELETE	/tasks/{id}/	Удалить задачу по ID	destroy
# /api/tasks/?status=in_progress сортировка по статусу
# /api/tasks/?order_by=created_at&order_direction=desc Сортировка по дате создания:
# api/tasks/?status=in_progress&order_by=created_at&order_direction=asc комбинированный запрос