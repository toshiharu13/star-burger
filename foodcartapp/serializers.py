from rest_framework import serializers
from rest_framework.serializers import ListField, ModelSerializer

from foodcartapp.models import FoodOrder, FoodOrderProduct


class OrderSerialisator(ModelSerializer):
    class Meta:
        model = FoodOrderProduct
        fields = ['product', 'quantity']


class ProductSerialiser(ModelSerializer):
    products = OrderSerialisator(many=True, allow_empty=False, write_only=True)

    class Meta:
        model = FoodOrder
        fields = ['firstname', 'lastname', 'phonenumber', 'address', 'products']

