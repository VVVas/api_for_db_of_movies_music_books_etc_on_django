from django.contrib.auth.models import AbstractUser
from django.db import models


USER_ROLE = 'user'
MODERATOR_ROLE = 'moderator'
ADMIN_ROLE = 'admin'

class User(AbstractUser):
    ROLES = [
        (USER_ROLE, 'Пользователь'),
        (MODERATOR_ROLE, 'Модератор'),
        (ADMIN_ROLE, 'Администратор')
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
        default=USER_ROLE,
        choices=ROLES,
        max_length=15,
        blank=False
    )

    @property
    def is_admin(self):
        return self.role == ADMIN_ROLE

    @property
    def is_moderator(self):
        return self.role == MODERATOR_ROLE

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
