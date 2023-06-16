import re
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator
from reviews.models import Category, Genre, Title, Review


from users.models import User


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField(max_length=254)
    first_name = serializers.CharField(max_length=150, required=False)
    last_name = serializers.CharField(max_length=150, required=False)

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

    def update(self, user, validated_data):
        user = User.objects.get(username=user)
        if validated_data.get("username"):
            user.email = validated_data.get("username")
        if validated_data.get("email"):
            user.email = validated_data.get("email")
        if validated_data.get("first_name"):
            user.first_name = validated_data.get("first_name")
        if validated_data.get("last_name"):
            user.last_name = validated_data.get("last_name")
        if validated_data.get("bio"):
            user.last_name = validated_data.get("bio")
        user.save()

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'role')
        extra_kwarg = {'email': {'required': True, 'allow_blank': False}}
        extra_kwarg = {'username': {'required': True, 'allow_blank': False}}


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
