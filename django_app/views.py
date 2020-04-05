# django_app/views.py

from django.views.generic import ListView, TemplateView
from .models import KeyWord, Tenders
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from datetime import date, datetime
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

class HomePageView(ListView):
    model = Tenders
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        context['tenders_list'] = Tenders.objects.all().exclude(price__iexact='0')[
            :4]
        return context


class AboutPageView(TemplateView):
    """Notes about about - html page"""
    template_name = 'about.html'


class WorkflowPageView(TemplateView):
    """Notes about workflow - html page"""
    template_name = 'workflow.html'


def search(request):
    """
    Our GET request will be like this
    http://127.0.0.1:8000/listings/search?keyword=pool&city=
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
            queryset_list = queryset_list.filter(
                description__icontains=keywords)

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
    queryset = Tenders.objects.order_by('-deadline').filter(deadline__gte=date.today())
    print('request.GET', request.GET)

    if 'keywords' in request.GET:
        keywords = request.GET['keywords']
        print('request.GET[keywords]', request.GET['keywords'])

        # if keywords not empty we'll filter by keywords by field "description"
        if keywords:
            queryset = queryset.filter(description__icontains=keywords)

    context = {
        'tenders': queryset,
        'values': request.GET
    }
    return render(request, 'simple_search.html', context)


def extended_search(request):
    listings = Tenders.objects.all()
    context = {}
    query = request.GET

    if query is not None:

        # ----------- state 0, 1, 2 --------------------------------
        if 'state' in query:
            state = query['state']
            if state == '0':
                listings = Tenders.objects.order_by('-deadline').filter(deadline__gte=date.today())
            elif state == '1':
                listings = Tenders.objects.order_by('-deadline').filter(deadline__lte=date.today())
            elif state == '2':
                listings = Tenders.objects.order_by('-deadline')

        # ----------- keyword --------------------------------
        if 'keyword' in query:
            keyword = query['keyword']
            if keyword:
                listings = listings.filter(description__icontains=keyword)

        # ----------- number --------------------------------
        if 'number' in query:
            number = query['number']
            if number:
                listings = listings.filter(number__icontains=number)

        # ----------- categories --------------------------------
        # code here

        # Pagination
        # remember last query for pagination
        context['last_query'] = '&'
        for key, value in query.items():
            # page is not needed because will be added in html
            if key != 'page':
                context['last_query'] += key + '=' + value + '&'
        context['last_query'] = context['last_query'][:-1]

        paginator = Paginator(listings, 10)
        page = query.get('page', 1)
        try:
            paged_listings = paginator.page(page)
        except PageNotAnInteger:
            paged_listings = paginator.page(1)
        except EmptyPage:
            paged_listings = paginator.page(paginator.num_pages)

        # Prepare context for transfering to html
        context['listings'] = paged_listings
        context['values'] = request.GET

        # print('last_query', context['last_query'])
        # print('Keys', context.keys())
    return render(request, 'extended_search.html', context)
