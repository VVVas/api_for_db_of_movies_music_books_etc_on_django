from django.contrib import admin
from django.contrib.auth import get_user_model

User = get_user_model()


# Мы все модели подключили к админке в файлах admin.py
# в соответствующих приложениях. Или надо было как-то по другом?
admin.site.register(User)
