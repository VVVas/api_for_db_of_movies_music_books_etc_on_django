from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from rest_framework.permissions import IsAuthenticatedOrReadOnly

from reviews.models import Category, Genre, Title
from .mixins import ListCreateDestroyViewSet
from .permissions import (
    IsAdminOrReadOnly, IsModeratorOrReadOnly, IsAuthorOrReadOnly
)
from .serializers import (SignUPSerializer,
                          CategorySerializer, GenreSerializer,
                          TitlesEditorSerializer, TitlesReadSerializer,
                          ReviewSerializer)

from users.models import User


class SignUPViewSet(viewsets.ModelViewSet):
    serializer_class = SignUPSerializer

    def perform_create(self, serializer):
        # Создание пользователя
        # Отправка confirmtion_code на email
        serializer.save(email=self.request.email, username=self.request.user)


class CategoryViewSet(ListCreateDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(ListCreateDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PATCH']:
            return TitlesEditorSerializer
        return TitlesReadSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly,
        IsModeratorOrReadOnly, IsAdminOrReadOnly
    )

    def _get_title_for_review(self):
        title_id = self.kwargs.get('title_id')
        return get_object_or_404(Title, id=title_id)

    def get_queryset(self):
        title = self._get_title_for_review()
        return title.review.select_related(
            'author',
        )

    def perform_create(self, serializer):
        title = self._get_title_for_review()
        serializer.save(author=self.request.user, title=title)
