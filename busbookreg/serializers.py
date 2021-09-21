from django.db.models import fields
from rest_framework import serializers
from .models import *

class Serializermodel(serializers.ModelSerializer):
    class Meta:
        model = Bus_booking
        fields = ('StartingLocation','EndLocation')
        

    def validate_StartingLocation(self,value):
        value=value.lower().replace(" ","")
        try:
            val=stoppagename[value]
            return val
        except Exception as err:
            print(err)
            raise serializers.ValidationError("No such Location Found")

    def validate_EndLocation(self,value):
        value=value.lower().replace(" ","")
        try:
            val=stoppagename[value]
            return val
        except Exception as err:
            raise serializers.ValidationError("No such Location Found")

    def create(self, validated_data):
        print(validated_data)
        return Bus_booking.Bus_book_tool.create(**validated_data)
        

    # # -https://opensource.com/article/20/11/django-rest-framework-serializers
    #https://www.django-rest-framework.org/api-guide/serializers/