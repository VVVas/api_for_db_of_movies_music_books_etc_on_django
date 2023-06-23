from django.urls import include, path
from rest_framework import routers

from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    GetTokenViewSet, ReviewViewSet, SignUPViewSet,
                    TitleViewSet, UsersViewSet)

from .messages import (URLS_SIGNUP, URLS_TOKEN, URLS_API)

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
    path(URLS_SIGNUP, SignUPViewSet.as_view()),
    path(URLS_TOKEN, GetTokenViewSet.as_view()),
    path(URLS_API, include(router_version_1.urls)),
]
