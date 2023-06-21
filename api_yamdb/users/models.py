from django.contrib.auth.models import AbstractUser
from django.db import models

ROLES = [
    ('user', 'Пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Администратор')
]


class User(AbstractUser):
    username = models.CharField(
        max_length=150,
        unique=True
    )
    email = models.CharField(
        max_length=254,
        unique=True
    )
    bio = models.TextField(
        verbose_name='Биография',
        help_text='Поле для биографии',
        blank=True
    )
    role = models.CharField(
        verbose_name='Роль',
        help_text='Поле для ввода роли (user, moderator, admin)',
        default='user',
        choices=ROLES,
        max_length=15,
        blank=False
    )

    @property
    def is_admin(self):
        return self.role == 'admin'

    @property
    def is_moderator(self):
        return self.role == 'moderator'

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
