from django.urls import include, path
from rest_framework import routers

from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    GetTokenViewSet, ReviewViewSet, SignUPViewSet,
                    TitleViewSet, UsersViewSet)

app_name = 'api'

router = routers.DefaultRouter()
router.register('users', UsersViewSet, basename='users')
router.register('categories', CategoryViewSet, basename='categories')
router.register('genres', GenreViewSet, basename='genres')
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router.register('titles', TitleViewSet, basename='titles')

auth_patterns = [
    path('signup/', SignUPViewSet.as_view()),
    path('token/', GetTokenViewSet.as_view()),
]

urlpatterns = [
    path('v1/auth/', include(auth_patterns)),
    path('v1/', include(router.urls)),
]
