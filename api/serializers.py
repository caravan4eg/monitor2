# api/serializers.py
from rest_framework import serializers
from django_app.models import Tenders, KeyWord
from django.utils.timesince import timeuntil


class TenderSerializer(serializers.ModelSerializer):

    time_left = serializers.SerializerMethodField()

    def get_time_left(self, object):
        time_delta = timeuntil(object.deadline)
        return time_delta

    class Meta:
        model = Tenders
        # fields = '__all__'
        exclude = ('created_at', 'updated_at')


class CategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = KeyWord
        fields = '__all__'
