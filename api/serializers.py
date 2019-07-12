# api/serializers.py
from rest_framework import serializers
from django_app.models import Tenders
 
class TendersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tenders
        # fields = ('number',)
        fields = '__all__'
