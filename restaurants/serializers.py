from rest_framework import serializers
from .models import Restaurant, MenuItem



class RestaurantSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False) 

    class Meta:
        model = Restaurant
        fields = '__all__'



class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = '__all__'

