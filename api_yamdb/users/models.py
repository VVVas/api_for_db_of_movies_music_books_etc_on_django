from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLES = [
        ('user', 'Пользователь'),
        ('moderator', 'Модератор'),
        ('admin', 'Администратор')
    ]
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
        help_text='Расскажите о себе, своих достижениях и т.д.',
        blank=True
    )
    role = models.CharField(
        verbose_name='Роль',
        help_text='Выберите роль: Пользователь, Модератор, Администратор',
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
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'],
                name='%(app_label)s_%(class)s_username_email_pair_unique'
            )
        ]
        ordering = ['username', 'id']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
