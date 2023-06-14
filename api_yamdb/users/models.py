from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    bio = models.TextField(
        verbose_name='Биография',
        help_text='Поле для биографии',
        blank=True
    )
    role = models.TextField(
        verbose_name='Роль',
        help_text='Поле для ввода роли (user, moderator, admin)',
        default='user',
        blank=False
    )

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
