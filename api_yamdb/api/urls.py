from django.urls import include, path
from rest_framework import routers

from api.views import (CategoryViewSet, GenreViewSet, TitleViewSet)


router_version_1 = routers.DefaultRouter()
router_version_1.register('categories', CategoryViewSet,
                          basename='categories')
router_version_1.register('genres', GenreViewSet, basename='genres')
router_version_1.register('titles', TitleViewSet, basename='titles')


urlpatterns = [
    path('v1/', include(router_version_1.urls)),
]
