# django_app/urls.py
from django.urls import path
from .views import HomePageView, AboutPageView, search
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings



urlpatterns = [
               path('', HomePageView.as_view(), name='home'),
               path('about/', AboutPageView.as_view(), name='about'),
               path('search', search, name='search'),
           ]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
