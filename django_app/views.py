# -*- coding: utf-8 -*-
# django_app/views.py

from django.views.generic import ListView, TemplateView
from .models import KeyWord, Tenders
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from datetime import date, datetime


class HomePageView(ListView):
    model = Tenders
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        context['tenders_list'] = Tenders.objects.all().exclude(price__iexact='0')[:4]
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


# class SimpleSearch(ListView):
#     model = Tenders
#     template_name = 'search.html'

#     def get_context_data(self, **kwargs):
#         context = super(HomePageView, self).get_context_data(**kwargs)
#         context['tenders_list'] = Tenders.objects.order_by('-deadline').filter(deadline__gte=date.today())

#         .filter(description__icontains=keywords)
#         return context


def simple_search(request):
    queryset = Tenders.objects.all().filter(deadline__gte=date.today())
    print('request.GET', request.GET)

    if 'keywords' in request.GET:
        keywords = request.GET['keywords']
        print('request.GET[keywords]', request.GET['keywords'])

        # if keywords not empty we'll filter by keywords by field "description"
        if keywords:
            queryset = queryset.filter(description__icontains=keywords)

    context = {
        # items from DB after all previously made filters
        'tenders': queryset,

        # transfer back all requested params to display them in form
        'values': request.GET
    }
    return render(request, 'simple_search.html', context)


def extended_search(request):
    queryset = Tenders.objects.all()
    query = request.GET
    print('*' * 50)
    print('state: ', query['state'])
    print('keywords:', query['keywords'])
    print('customer:', query['customer'])
    print('number:', query['number'])
    print('*' * 50)

    def get_queryset(self):
        """
        url -> http://127.0.0.1:8000/api/v1/search/?description=lan&query=asutp
        - self.request.GET
        - self.request.query_params
        return the same dict <QueryDict:
        -> {'description': ['lan'], 'query': ['asutp']}>
        - self.request.GET.get("query") -> returns value of query param
        -> asutp
        state 0,1,2:
            actual tenders state = 0
            archive tenders state = 1
            all tenders actual and archive state = 2
        """
        query = self.request.GET

        queryset = Tenders.objects.all()[:5]
        print(len(queryset))
        if not query:
            return queryset

        # ----------- state 0, 1, 2 --------------------------------
        if 'state' in query:
            state = query['state']
            print('State: ', state)
            if state == '0':
                queryset = queryset.filter(deadline__gte=date.today())
            elif state == '1':
                queryset = queryset.filter(deadline__lte=date.today())
            elif state == '2':
                pass
        # ----------- state 0, 1, 2 --------------------------------

        # Requested categories
        if 'categories' in query:
            categories = query['categories']
            print('Requested categories: ', categories)
            if 'all' in categories:
                queryset = queryset

        # Filter tender list by keywords in description
        if 'keywords' in query:
            keywords = query['keywords']
            print('Requested keywords: ', keywords)
            if keywords:
                queryset = queryset.filter(description__icontains=keywords)

        return queryset

    context = {
        # items from DB after all previously made filters
        'tenders': queryset[:5],

        # transfer back all requested params to display them in form
        'values': request.GET
    }
    return render(request, 'extended_search.html', context)
