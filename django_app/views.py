# django_app/views.py
from django.views.generic import ListView, TemplateView
from .models import KeyWord, Tenders
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404


class HomePageView(ListView):
    model = Tenders
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        context['tenders_list'] = Tenders.objects.order_by('-deadline')[:3]
        return context


class AboutPageView(TemplateView):
    """Notes about workflow - html page"""
    template_name = 'about.html'

def search(request):
    """
    Our GET request will be like this
    http://127.0.0.1:8000/listings/search?keywords=pool&city=
    We will look if there is "keywords" or another query params are in request and then filter by them.
    All query params are there in request dict like this:
        <QueryDict: {'keywords': ['pool, garage'], 'city': ['']}>
    """
    # get all items from DB
    queryset_list = Tenders.objects.all()

    if 'keywords' in request.GET:
        keywords = request.GET['keywords']
        print(request.GET['keywords'])

        # if keywords not empty we'll filter by keywords by field "description"
        if keywords:
            queryset_list = queryset_list.filter(description__icontains=keywords)

    # Filter by City
    if 'city' in request.GET:
        city = request.GET['city']
        if city:
            queryset_list = queryset_list.filter(city__iexact=city)

    # Filter by State
    if 'state' in request.GET:
        state = request.GET['state']
        if state:
            queryset_list = queryset_list.filter(state__iexact=state)

    # Filter by Bedrooms
    if 'bedrooms' in request.GET:
        bedrooms = request.GET['bedrooms']
        if bedrooms:
            # bedrooms__lte (less then equals)
            queryset_list = queryset_list.filter(bedrooms__lte=bedrooms)

    # Filter by Price
    if 'price' in request.GET:
        price = request.GET['price']
        if price:
            # price__lte (less then equals)
            queryset_list = queryset_list.filter(price__lte=price)

    context = {
        # data from listings/choices.py for search form
        'bedroom_choices': bedroom_choices,
        'state_choices': state_choices,
        'price_choices': price_choices,

        # items from DB after all previously made filters
        'listings': queryset_list,

        # transfer back all requested params to display them in form
        'values': request.GET
    }
    return render(request, 'listings/search.html', context)
