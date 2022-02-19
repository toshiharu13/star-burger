from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import ListField

from foodcartapp.models import FoodOrderProduct, FoodOrder


class OrderSerialisator(ModelSerializer):
    class Meta:
        model = FoodOrderProduct
        fields = ['product', 'quantity']


class ProductSerialiser(ModelSerializer):
    products = OrderSerialisator(many=True, allow_empty=False, write_only=True)

    class Meta:
        model = FoodOrder
        fields = ['firstname', 'lastname', 'phonenumber', 'address', 'products']

