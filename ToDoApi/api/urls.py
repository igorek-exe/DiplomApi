from django.urls import path, include

from api.views import UserListView, CustomUserViewSet, TasksApiView

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
    path('tasks/', TasksApiView.as_view())

]
# http://127.0.0.1:8000/api/token/login/ получение токена
# /api/token/logout/ удаление токена
#/api/users/set_password/ изменить пароль юзера
# {
#     "current_password": "your_current_password",
#     "new_password": "your_new_password"
# }
#/api/users/reset_password/ сбросить пароль юзера
# /api/users/reset_password_confirm/
# {
#     "new_password": "your_new_password_here",
#     "uid": "MTk",  // ваш закодированный uid
#     "token": "ceea5y-242c6f5c97e5ceff179b0134fcf752fe"  // ваш токен
# }

