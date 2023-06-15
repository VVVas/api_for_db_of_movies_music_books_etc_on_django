from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from reviews.models import Category, Genre, Title
from .mixins import ListCreateDestroyViewSet
from .permissions import (
    IsAdminOrReadOnly, IsModeratorOrReadOnly, IsAuthorOrReadOnly
)
from .serializers import (SignUPSerializer, GetTokenSerializer,
                          CategorySerializer, GenreSerializer,
                          TitlesEditorSerializer, TitlesReadSerializer,
                          ReviewSerializer)

from users.models import User


class SignUPViewSet(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SignUPSerializer(data=request.data)
        if serializer.is_valid():
            user = request.data['username']
            email = request.data['email']
            # Создаем нового пользователя
            user_obj = User.objects.create(username=user, email=email)
            # Получаем на него токен подтверждение
            confirmation_code = default_token_generator.make_token(user_obj)
            print(confirmation_code)
            # Отправка confirmtion_code на email
            send_mail(
                'Регистрация пользователя',
                f'Привет, {user}!\n\n confirmation_code = {confirmation_code}.',
                'admin@yamdb.ru',
                [email],
                fail_silently=False,  # Сообщать об ошибках («молчать ли об ошибках?»)
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class GetTokenViewSet(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = GetTokenSerializer(data=request.data)
        if serializer.is_valid():
            user = request.data['username']
            confirmation_code = request.data['confirmation_code']
            user_obj = User.objects.get(username=user)
            # Проверка confirmation_code
            if default_token_generator.check_token(user_obj, confirmation_code):
                # Получение токена
                refresh = RefreshToken.for_user(user_obj)
                response = {
                    'token': str(refresh.access_token)
                }
                # Выдача токена
                return Response(response)
            else:
                return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
