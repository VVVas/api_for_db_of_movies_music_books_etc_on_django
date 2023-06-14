from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from .serializers import SignUPSerializer
from users.models import User


class SignUPViewSet(viewsets.ModelViewSet):
    serializer_class = SignUPSerializer

    def perform_create(self, serializer):
        # Создание пользователя
        # Отправка confirmtion_code на email
        serializer.save(email=self.request.email, username=self.request.user)
