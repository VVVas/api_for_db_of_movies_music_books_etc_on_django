from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from reviews.models import Category, Genre
from .mixins import ListCreateDestroyViewSet
from .permissions import (IsAdminOrReadOnly)
from .serializers import (SignUPSerializer,
                          CategorySerializer, GenreSerializer,
                          TitlesEditorSerializer, TitlesReadSerializer)

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
