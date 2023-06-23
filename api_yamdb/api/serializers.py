import re
from datetime import datetime

from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from reviews.models import Category, Comment, Genre, Review, Title
from .messages import (ERR_REVIEW_ONE, ERR_REVIEW_SCORE,
                       ERR_TITLE_YEAR_FROM_FUTURE, ERR_USER_EMAIL_UNIQUE,
                       ERR_USER_NAME_NOT_ME, ERR_USER_NAME_TEMPLATE,
                       ERR_USER_NAME_UNIQUE, RE_USER_NAME_TEMPLATE)

User = get_user_model()


def _username_check(self, value):
    if value == settings.USER_SELF:
        raise serializers.ValidationError(ERR_USER_NAME_NOT_ME)
    elif not re.fullmatch(RE_USER_NAME_TEMPLATE, value):
        raise serializers.ValidationError(ERR_USER_NAME_TEMPLATE)
    return value


class UserSerializer(serializers.ModelSerializer):

    def validate_username(self, value):
        return _username_check(self, value)

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role',
        )
        extra_kwarg = {'email': {'required': True, 'allow_blank': False}}
        extra_kwarg = {'username': {'required': True, 'allow_blank': False}}


class SignUPSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=254)
    username = serializers.CharField(max_length=150)

    def validate_username(self, value):
        return _username_check(self, value)

    def validate(self, data):
        if User.objects.filter(email=data['email']).exclude(
                username=data['username']).exists():
            raise serializers.ValidationError(ERR_USER_EMAIL_UNIQUE)
        if User.objects.filter(username=data['username']).exclude(
                email=data['email']).exists():
            raise serializers.ValidationError(ERR_USER_NAME_UNIQUE)
        return data

    class Meta:
        model = User
        fields = ('email', 'username')
        extra_kwarg = {'email': {'required': True, 'allow_blank': False}}
        extra_kwarg = {'username': {'required': True, 'allow_blank': False}}


class GetTokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField()

    def validate_username(self, value):
        return _username_check(self, value)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')
        extra_kwarg = {'username': {'required': True, 'allow_blank': False}}
        extra_kwarg = {
            'confirmation_code': {'required': True, 'allow_blank': False}
        }


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ('id',)
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        exclude = ('id',)
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class TitlesReadSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = '__all__'


class TitlesEditorSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all(),
    )

    def validate_year(self, value):
        if value > (datetime.now().year + 10):
            raise serializers.ValidationError(ERR_TITLE_YEAR_FROM_FUTURE)
        return value

    class Meta:
        model = Title
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )

    def validate_score(self, value):
        if value < 0 or value > 10:
            raise serializers.ValidationError(ERR_REVIEW_SCORE)
        return value

    def validate(self, data):
        request = self.context['request']
        title_id = self.context['view'].kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        if request.method == 'POST':
            if request.user.reviews.filter(
                    title=title).exists():
                raise serializers.ValidationError(ERR_REVIEW_ONE)
        return data

    class Meta:
        exclude = ('title',)
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )

    class Meta:
        exclude = ('review',)
        model = Comment
