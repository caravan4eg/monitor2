# from django.urls import path
# from .views import TendersAPIView


# urlpatterns = [
#         path('', TendersAPIView.as_view(), name='api'),

#     ]

# # old

from django.urls import path
from .views import (
                    ApiRoot,
                    CategoryList,
                    CategoryDetail,
                    DemoTendersList,
                    FilteredTenderList,
                    Search,
               )


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

               path('tenders/demo',
                    DemoTendersList.as_view(),
                    name=DemoTendersList.name),

               path('search',
                    Search.as_view(),
                    name=Search.name),





    ]
