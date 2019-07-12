"""django_project URL Configuration

"""
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('django_app.urls')),
    path('api/v1/', include('api.urls')),
]
