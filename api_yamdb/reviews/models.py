from datetime import datetime

from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

User = get_user_model()


class GenreCategoryBaseClass(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Название'
    )
    slug = models.SlugField(
        max_length=50,
        verbose_name='ID',
        unique=True
    )

    def __str__(self):
        return self.name

    class Meta:
        abstract = True
        ordering = ['name']


class ReviewCommentBaseClass(models.Model):
    text = models.TextField(verbose_name='Текст')
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата')

    class Meta:
        abstract = True
        ordering = ['-pub_date', 'id']

    def __str__(self) -> str:
        return self.text[:15]


class Category(GenreCategoryBaseClass):

    class Meta(GenreCategoryBaseClass.Meta):
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(GenreCategoryBaseClass):

    class Meta(GenreCategoryBaseClass.Meta):
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Название'
    )
    year = models.SmallIntegerField(
        verbose_name='Год выпуска',
        validators=(
            MaxValueValidator(
                (datetime.now().year + 10),
                'Год слишком далеко в будущем'
            ),
        ),
    )
    description = models.TextField(
        verbose_name='Описание',
        null=True,
        blank=True
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанр'
    )
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        on_delete=models.SET_NULL,
        related_name='titles',
        null=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ['name']


class Review(ReviewCommentBaseClass):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор'
    )
    score = models.PositiveSmallIntegerField(
        verbose_name='Оценка',
        validators=(
            MinValueValidator(1, 'Минимальная оценка - 1'),
            MaxValueValidator(10, 'Наивысшая оценка - 10'),
        ),
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='%(app_label)s_%(class)s_author_title_pair_unique'
            )
        ]
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'


class Comment(ReviewCommentBaseClass):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор'
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв'
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
