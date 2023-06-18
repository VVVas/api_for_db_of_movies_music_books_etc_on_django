from django.urls import include, path
from rest_framework import routers

from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    GetTokenViewSet, ReviewViewSet, SignUPViewSet,
                    TitleViewSet, UsersViewSet)

app_name = 'api'

router_version_1 = routers.DefaultRouter()
router_version_1.register('users', UsersViewSet, basename='users')
router_version_1.register('categories', CategoryViewSet, basename='categories')
router_version_1.register('genres', GenreViewSet, basename='genres')
router_version_1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)
router_version_1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router_version_1.register('titles', TitleViewSet, basename='titles')


urlpatterns = [
    # Регистрация нового пользователя и cотправка формы на email
    path('v1/auth/signup/', SignUPViewSet.as_view()),
    # Получение токена
    path('v1/auth/token/', GetTokenViewSet.as_view()),
    # Работа с пользователем
    path('v1/', include(router_version_1.urls)),
]
