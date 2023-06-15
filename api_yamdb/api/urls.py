from django.urls import path, include
from rest_framework import routers
from .views import SignUPViewSet, GetTokenViewSet

from api.views import (CategoryViewSet, GenreViewSet, TitleViewSet)

app_name = 'api'
  
router_version_1 = routers.DefaultRouter()
router_version_1.register('categories', CategoryViewSet,
                          basename='categories')
router_version_1.register('genres', GenreViewSet, basename='genres')
router_version_1.register('titles', TitleViewSet, basename='titles')


urlpatterns = [
    # Регистрация нового пользователя и cотправка формы на email
    path('v1/auth/signup/', SignUPViewSet.as_view()),
    # Получение токена
    path('v1/auth/token/', GetTokenViewSet.as_view()),
    path('v1/', include(router_version_1.urls)),
]
