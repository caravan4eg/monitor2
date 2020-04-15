# from django_filters.rest_framework import DjangoFilterBackend, FilterSet
# from django_app.models import Tenders
# # from django_filters import CharFilter, BaseInFilter
# from django.db import models
# from django_app.models import Tenders



# class SomewordsFilter(BaseInFilter, CharFilter):
#     pass


# class SearchFilter(FilterSet):
#     # multiple search doesn't work
#     # looks up only obe field
#     # description_contains = SomewordsFilter(field_name='description',
#                                         #    lookup_expr='icontains')

#     # single search works
#     description_contains = CharFilter(field_name='description',
#                                            lookup_expr='icontains')

#     class Meta:
#         filter_overrides = {
#              models.CharField: {
#                  'filter_class': CharFilter,
#                  'extra': lambda f: {
#                      'lookup_expr': 'icontains',
#                  },
#              },
#         }


# class byWordFilter(FilterSet):
#     """ Filters all tenders by all fields by given word in Filters form
#         or from GET request like this:
#         .../api/tenders/all-valid?description='enter word here'
#     """

#     description = CharFilter(field_name='description',
#                             lookup_expr='icontains')

#     # so you can add new field in filter in Filters at brawseable api view
#     # number_contains = CharFilter(field_name='number',
#     #                                   lookup_expr='contains')
#     # and after add field to Meta field

#     class Meta:
#         model = Tenders
#         fields = ()


# ==================== is it used?
# class KeywordsInFilter(BaseInFilter, CharFilter):
#     pass


# class FilterIn(FilterSet):
#     keywords_in_description = KeywordsInFilter(field_name='description',
#                                                lookup_expr='in')

#     class Meta:
#         model = Tenders
#         fields = ['keywords_in_description',
#                   ]
