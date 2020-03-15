# from django.urls import path
# from .views import TendersAPIView


# urlpatterns = [
#         path('', TendersAPIView.as_view(), name='api'),

#     ]

# # old

from django.urls import path
from .views import (
                    AllTendersList,
                    ApiRoot,
                    CategoryList,
                    CategoryDetail,
                    DemoTendersList,
                    FilteredTenderList,
                    TenderList,)


urlpatterns = [

               path('',
                    ApiRoot.as_view(),
                    name=ApiRoot.name),

               path('categories/',
                    CategoryList.as_view(),
                    name=CategoryList.name),

               path('categories/<int:pk>/',
                    CategoryDetail.as_view(),
                    name=CategoryDetail.name),

               # without any filters and invalid tenders too
               path('tenders/all/',
                    AllTendersList.as_view(),
                    name=AllTendersList.name),

               path('tenders/all-valid/',
                    TenderList.as_view(),
                    name=TenderList.name),

               path('tenders/demo',
                    DemoTendersList.as_view(),
                    name=DemoTendersList.name),

               # path('tenders/<tenders_by_categories>/',
               #      FilteredTenderList.as_view(),
               #      name=FilteredTenderList.name),
               path('search',
                    FilteredTenderList.as_view(),
                    name=FilteredTenderList.name),


    ]
