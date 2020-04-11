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
        context['tenders_list'] = Tenders.objects.all().exclude(price__iexact='0').filter(deadline__gte=date.today())[:4]
        return context


class AboutPageView(TemplateView):
    """Notes about about - html page"""
    template_name = 'about.html'


class WorkflowPageView(TemplateView):
    """Notes about workflow - html page"""
    template_name = 'workflow.html'


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
    context = {}
    query = request.GET
    print('request.GET', request.GET)

    if 'keywords' in request.GET:
        keywords = request.GET['keywords']
        print('request.GET[keywords]', request.GET['keywords'])

        # if keywords not empty we'll filter by keywords by field "description"
        if keywords:
            queryset = queryset.filter(description__icontains=keywords)

    # # ----------- Pagination --------------------------------
        # safe last query for pagination
        context['last_query'] = '&'
        for key, value in query.items():
            # page from request is not needed now because will be added in html
            if key != 'page':
                context['last_query'] += key + '=' + value + '&'
        context['last_query'] = context['last_query'][:-1]
        print(context['last_query'])

        paginator = Paginator(queryset, 5)
        page = query.get('page', 1)
        try:
            paged_queryset = paginator.page(page)
        except PageNotAnInteger:
            paged_queryset = paginator.page(1)
        except EmptyPage:
            paged_queryset = paginator.page(paginator.num_pages)
    context['listings'] = paged_queryset
    context['values'] = request.GET
    return render(request, 'simple_search.html', context)


def extended_search(request):
    listings = Tenders.objects.all()
    context = {}
    query = request.GET

    if query is not None:

        # ----------- filter by  state 0, 1, 2 --------------------------------
        if 'state' in query:
            state = query['state']
            if state == '0':
                listings = Tenders.objects.order_by('-deadline').filter(deadline__gte=date.today())
            elif state == '1':
                listings = Tenders.objects.order_by('-deadline').filter(deadline__lte=date.today())
            elif state == '2':
                listings = Tenders.objects.order_by('-deadline')

        # ----------- categories --------------------------------
        selected_categories = [key for key, value in query.items() if value == 'on']
        if selected_categories:
            print(f'{"*"*30} Selected category: {selected_categories}')


            # get plus and minus keywords for selected category from DB
            for category in selected_categories:
                obj = KeyWord.objects.get(category_name__startswith=category)
                plus_keywords = [word.strip() for word in obj.plus_keywords.split(',')]
                minus_keywords = [word.strip() for word in obj.minus_keywords.split(',')]
            print('************ Keywords for selected category: ')
            print('Plus keywords:', plus_keywords)
            print('Minus keywords:', minus_keywords)

            # filter by plus_keywords
            # TODO: improve filter
            #       now filters both by "IP":
            #       ip networks -> good
            #       PhilIPs -> bad
            # or deep learning?
            wanted_items = set()
            for word in plus_keywords:
                try:
                    for item in listings.filter(description__icontains=word):
                        print('----------------------------------------------')
                        print('Tender filtered by word: ', word)
                        print('Number: ', item.number)
                        print('Description: ', item.description)
                        print('----------------------------------------------\n')

                        wanted_items.add(item.pk)
                except:
                    continue
            listings = listings.filter(pk__in=wanted_items)

            # TODO: add using minus word
            # # for word in minus_keywords:
            # #     for item in wanted_items:
            # #         if word in item:
            # #             wanted_items.remove(item.pk)

        # ----------- filter by keyword --------------------------------
        if 'keyword' in query:
            keyword = query['keyword']
            if keyword:
                listings = listings.filter(description__icontains=keyword)

        # ----------- filter by number --------------------------------
        if 'number' in query:
            number = query['number']
            if number:
                listings = listings.filter(number__icontains=number)

        # ----------- filter by customer --------------------------------
        if 'customer' in query:
            customer = query['customer']
            if customer:
                listings = listings.filter(customer__icontains=customer)

        # ----------- Pagination --------------------------------
        # safe last query for pagination
        context['last_query'] = '&'
        for key, value in query.items():
            # page from request is not needed now because will be added in html
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
