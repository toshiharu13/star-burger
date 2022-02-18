from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from foodcartapp.models import Product, FoodOrder


class ProductSerialiser(ModelSerializer):
    class Meta:
        model = FoodOrder
        fields = ['firstname', 'lastname', 'phonenumber', 'address']
