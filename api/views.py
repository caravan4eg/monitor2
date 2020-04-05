# api/views.py
from rest_framework import generics
from django_app.models import Tenders, KeyWord
from .serializers import TenderSerializer, CategorySerializer

from datetime import date, datetime
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django_filters.rest_framework import DjangoFilterBackend
# from url_filter.integrations.drf import DjangoFilterBackend
from .filters import SearchFilter, byWordFilter

from django_filters import rest_framework as filters
from django.db.models import Q

from rest_framework.viewsets import ModelViewSet

from django_filters import AllValuesFilter, DateTimeFilter, NumberFilter, CharFilter, BaseInFilter

#  old -----------------------------------------------


class TendersAPIView(generics.ListAPIView):
    queryset = Tenders.objects.all()
    serializer_class = TenderSerializer
#  old -----------------------------------------------


class CategoryList(generics.ListAPIView):
    """Categories list"""
    queryset = KeyWord.objects.all()
    serializer_class = CategorySerializer
    name = "All categories list"

    filter_backends = (filters.DjangoFilterBackend,)
    # filter_fields = ('category_name', 'category_descr',)
    search_fields = (
        '^category_name',
        '^category_descr',
    )


# TODO: потом сделать радактируемой только для администратора
class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    """Create, read, update, delete category"""
    queryset = KeyWord.objects.all()
    serializer_class = CategorySerializer
    name = "Category detail"


class DemoTendersList(generics.ListAPIView):
    """Last or more expensive valid tenders """
    queryset = Tenders.objects.order_by('-created_at').filter(deadline__gte=date.today())[:10]
    serializer_class = TenderSerializer
    name = 'Demo tenders-list'


class FilteredTenderList(generics.ListAPIView):
    """
    /tenders/'here one or some keywords' from list below:
    For example: <host>/api/v1/tenders/lan, asutp
        all,
        asutp,
        data
        centre,
        lan,
        soft,
        hardware,
        ventilation,
        security_alarm...

    """

    name = 'Tenders list filtered by categories'
    serializer_class = TenderSerializer

    filter_backends = (DjangoFilterBackend,)
    filter_class = byWordFilter

    def get_queryset(self):
        """
        This view should return a list of all tenders for
        categories as determined by the category_request portion of the URL.
        """
        # # proba
        # print(self.request.GET)
        # print(self.kwargs)

        wanted_items = set()
        category_list = (
            'all',
            'asutp',
            'data centre',
            'lan',
            'soft, hardware',
            'ventilation',
            'security_alarm'
        )

        # get list requested categories from GET request
        # and check if they are in category_list

        requested_categories = [
            category for category in category_list
            if category in self.kwargs['tenders_by_categories'].lower()
        ]

        if 'all' in requested_categories:
            return Tenders.objects.filter(deadline__gte=date.today())

        for category in requested_categories:
            obj = KeyWord.objects.get(category_name__startswith=category)
            plus_keywords = [word.strip()
                             for word in obj.plus_keywords.split(',')]
            minus_keywords = [word.strip()
                              for word in obj.minus_keywords.split(',')]
            print('Requested CATEGORY: ', category)

        # filter by plus_keywords
        # TODO: improve filter
        #           now filters both by IP:
        #           ip networks - good
        #           PhilIPs - bad
            for word in plus_keywords:
                for item in Tenders.objects.filter(
                    Q(deadline__gte=date.today()),
                    Q(description__icontains=word),
                ):
                    print('----------------------------------------------')
                    print('Tender filtered by word: ', word)
                    print('Number: ', item.number)
                    print('Description: ', item.description)
                    print('----------------------------------------------\n')

                    wanted_items.add(item.pk)

        # TODO: add using minus word
        # for word in minus_keywords:
        #     for item in wanted_items:
        #         if word in item:
        #             wanted_items.remove(item.pk)

        return Tenders.objects.filter(pk__in=wanted_items)


class Search(generics.ListAPIView):
    name = 'Search'
    serializer_class = TenderSerializer

    def get_queryset(self):
        """
        url -> http://127.0.0.1:8000/api/v1/search/?description=lan&query=asutp
        - self.request.GET
        - self.request.query_params
        return the same dict <QueryDict:
        -> {'description': ['lan'], 'query': ['asutp']}>
        - self.request.GET.get("query") -> returns value of query param
        -> asutp
        """
        query = self.request.GET
        queryset = Tenders.objects.all()
        if not query:
            return queryset

        # actual tenders state = 0
        # archive tenders state = 1
        # all tenders actual and archive state = 2
        if 'state' in query:
            state = query['state']
            print('State: ', state)
            if state == '0':
                queryset = queryset.filter(deadline__gte=date.today())
            elif state == '1':
                queryset = queryset.filter(deadline__lte=date.today())
            elif state == '2':
                pass

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


class ApiRoot(generics.GenericAPIView):
    # TODO: add info and docs about project
    """
        Routes:
        /search - search like this .../api/v1/search?keywords=Коагулянт&state=0
        /categories/ - all categories list
        /categories/'number'/ - category detail, CRUD
        /tenders/demo - list of 10 valid more expensive or newest tenders
        /tenders/'tenders_by_categories' - filter data by cetegory like this:
            all, lan, ventilation, asutp, data centre, soft, hardware, ventilation,
            security_alarm...

            Examples:
            /tenders/lan,asutp
            /tenders/soft,hardware
            /tenders/ventilation
      """
    name = 'TenderMonitor API-root'

    def get(self, request, *args, **kwargs):
        return Response({
                'search': reverse(Search.name, request=request),
                'all-category-list': reverse(CategoryList.name, request=request),
                'demo-tenders-list': reverse(DemoTendersList.name, request=request),
            })
