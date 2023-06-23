from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db import IntegrityError
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import Category, Genre, Review, Title
from .filters import TitleFilter
from .messages import EMAIL_CONF_CODE_MESSAGE, EMAIL_CONF_CODE_SUBJECT
from .permissions import (IsAdmin, IsAdminOrReadOnly,
                          IsAuthorModeratorAdminOrReadOnly)
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, GetTokenSerializer,
                          ReviewSerializer, SignUPSerializer,
                          TitlesEditorSerializer, TitlesReadSerializer,
                          UserSerializer)

User = get_user_model()


class SignUPViewSet(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = SignUPSerializer(data=request.data)
        if serializer.is_valid():
            username = request.data['username']
            email = request.data['email']
            user, _ = User.objects.get_or_create(
                username=username, email=email
            )

            # user = get_object_or_404(User, username=username, email=email)
            
            # try:
            #     user, _ = User.objects.get_or_create(
            #         username=username, email=email
            #     )
            # except IntegrityError:
            #     return Response(
            #         serializer.data, status=status.HTTP_400_BAD_REQUEST
            #     )
            confirmation_code = default_token_generator.make_token(user)
            send_mail(
                EMAIL_CONF_CODE_SUBJECT,
                EMAIL_CONF_CODE_MESSAGE + confirmation_code,
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetTokenViewSet(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = GetTokenSerializer(data=request.data)
        if serializer.is_valid():
            username = request.data['username']
            confirmation_code = request.data['confirmation_code']
            user = get_object_or_404(User, username=username)
            if default_token_generator.check_token(user, confirmation_code):
                refresh = RefreshToken.for_user(user)
                response = {
                    'token': str(refresh.access_token)
                }
                return Response(response)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    filter_backends = (SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'
    http_method_names = ['get', 'post', 'patch', 'delete']

    @action(
        detail=False,
        permission_classes=(IsAuthenticated,),
        methods=['get', 'patch'],
        url_path=settings.USER_SELF
    )
    def me(self, request):
        if request.method == 'GET':
            queryset = User.objects.all()
            user = get_object_or_404(queryset, username=request.user)
            serializer = UserSerializer(user)
        if request.method == 'PATCH':
            serializer = self.get_serializer(
                request.user, data=request.data, partial=True
            )
            if not serializer.is_valid():
                return Response(
                    serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )
            serializer.save(role=request.user.role)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GenreCategoryBaseViewSet(mixins.ListModelMixin,
                               mixins.CreateModelMixin,
                               mixins.DestroyModelMixin,
                               viewsets.GenericViewSet):
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class CategoryViewSet(GenreCategoryBaseViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(GenreCategoryBaseViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.select_related(
        'category',
    ).annotate(rating=Avg('reviews__score')).order_by('name')
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PATCH']:
            return TitlesEditorSerializer
        return TitlesReadSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorModeratorAdminOrReadOnly, )

    def _get_title_for_review(self):
        title_id = self.kwargs.get('title_id')
        return get_object_or_404(Title, id=title_id)

    def get_queryset(self):
        title = self._get_title_for_review()
        return title.reviews.select_related(
            'author',
        ).order_by('-pub_date', 'id')

    def perform_create(self, serializer):
        title = self._get_title_for_review()
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorModeratorAdminOrReadOnly, )

    def _get_review_for_comment(self):
        review_id = self.kwargs.get('review_id')
        return get_object_or_404(Review, id=review_id)

    def get_queryset(self):
        review = self._get_review_for_comment()
        return review.comments.select_related(
            'author',
        ).order_by('-pub_date', 'id')

    def perform_create(self, serializer):
        review = self._get_review_for_comment()
        serializer.save(author=self.request.user, review=review)
