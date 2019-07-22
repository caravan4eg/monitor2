# api/views.py
from rest_framework import generics
from django_app.models import Tenders, KeyWord
from .serializers import TenderSerializer, CategorySerializer

from datetime import date, datetime
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django_filters.rest_framework import DjangoFilterBackend
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
    today = date.today()
    queryset = Tenders.objects.filter(deadline__gte=today)[:10]
    serializer_class = TenderSerializer
    name = 'Demo tenders-list'
    

class TenderList(generics.ListAPIView):
    """All valid tenders list
    you can search by any word like this
    .../api/tenders/all-valid?search_word=Гродно
    """
    name = 'TenderList'
    serializer_class = TenderSerializer
    
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = byWordFilter
    
    def get_queryset(self):
        valid_tenders = Tenders.objects.filter(deadline__gte=date.today())
        return valid_tenders

    # появляется фильтр в закладке и хорошо ищет по слову или части 
    # тк в фильтре указано contains


    # появляются в фильтры ф закладке Filters, но так НЕ находит ничего
    # видимо ищет единстевнное слово а не вхождения 
    # filter_fields = ('description', 'customer',)
    # search_fields = ('^description',)


class AllTendersList(generics.ListAPIView):
    """All tenders list"""
    # without any filters
    queryset = Tenders.objects.all()
    serializer_class = TenderSerializer
    name = 'All tenders list'
    # search in tenders
    filter_backends = (DjangoFilterBackend,)
    filter_class = byWordFilter

class FilteredTenderList(generics.ListAPIView):
    """ /tenders/'here one or some keywords' from list below:
        all, asutp, data centre, lan, soft, hardware, ventilation, security_alarm...
        For example: <host>/api/tenders/lan,asutp
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
                                category.strip() for category in category_list 
                                if category in self.kwargs['tenders_by_categories'].lower()
                                ]
                
        if 'all' in requested_categories:
            return Tenders.objects.filter(deadline__gte=date.today())
        
        for category in requested_categories:
            obj = KeyWord.objects.get(category_name__startswith=category)
            plus_keywords = [word.strip() for word in obj.plus_keywords.split(',')]
            minus_keywords =[word.strip() for word in obj.minus_keywords.split(',')]
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


class ApiRoot(generics.GenericAPIView):
    # TODO: add info and docs about project
    """
        Routes:

        /categories/ - all categories list
        /categories/'number'/ - category detail, CRUD
        /tenders/demo - list of 10 valid more expensive or newest tenders
        /tenders/all/ - list of all tenders, invalid too
        /tenders/all-valid - list of all valid tenders 
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
                        'all-category-list': reverse(CategoryList.name,
                                                    request=request),

                        'all-tenders-list': reverse(AllTendersList.name,
                                                    request=request),

                        'demo-tenders-list': reverse(DemoTendersList.name,
                                                     request=request),

                        'valid-tender-list': reverse(TenderList.name,
                                                     request=request),
                           
                        })