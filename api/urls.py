from django.urls import path
from .views import TendersAPIView


urlpatterns = [
        path('', TendersAPIView.as_view(), name='api'),
    ]