# django_app/views.py
from django.views.generic import ListView, TemplateView
from .models import KeyWord, Tenders



class HomePageView(ListView):
    """Expose list of tenders from db - html page"""
    model = Tenders
    template_name = 'home.html'
    context_object_name = 'all_tenders_list' 


class AboutPageView(TemplateView):
    """Notes about workflow - html page"""
    template_name = 'about.html'