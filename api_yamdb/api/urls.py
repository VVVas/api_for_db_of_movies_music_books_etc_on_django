from django.urls import include, path
from .views import SignUPViewSet

app_name = 'api'

urlpatterns = [
    # Эндотип отправки формы на email
    path('v1/auth/signup/', SignUPViewSet),
]
