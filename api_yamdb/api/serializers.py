import re
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator
from reviews.models import Category, Genre, Title, Review


from users.models import User


class SignUPSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=254)
    username = serializers.CharField(max_length=150)

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Использовать имя me запрещено!'
            )
        elif not re.fullmatch(r'^[\w.@+-]+\Z', value):
            raise serializers.ValidationError(
                'Имя должно соответствовать шаблону!'
            )
        else:
            return value

    class Meta:
        model = User
        fields = ('email', 'username')
        extra_kwarg = {'email': {'required': True, 'allow_blank': False}}
        extra_kwarg = {'username': {'required': True, 'allow_blank': False}}


class GetTokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField()
    def validate_username(self, value):
        if not re.fullmatch(r'[\w.@+-]+\Z', value):
            raise serializers.ValidationError(
                'Имя должно соответствовать шаблону!'
            )
        else:
            return value

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')
        extra_kwarg = {'username': {'required': True, 'allow_blank': False}}
        extra_kwarg = {'confirmation_code': {'required': True, 'allow_blank': False}}


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

    class Meta:
        model = Title
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review
        validators = (
            serializers.UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=('author', 'title'),
                message='Разрешён только один Отзыв на Произведение',
            ),
        )
