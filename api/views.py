# api/views.py
from rest_framework import generics
from django_app.models import Tenders
from .serializers import TendersSerializer
 
class TendersAPIView(generics.ListAPIView):
    queryset = Tenders.objects.all()
    serializer_class = TendersSerializer


