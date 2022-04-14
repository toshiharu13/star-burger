from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.templatetags.static import static
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from foodcartapp.serializers import ProductSerialiser

from .models import (FoodOrder, FoodOrderProduct, Product, Restaurant,
                     RestaurantMenuItem)


def banners_list_api(request):
    # FIXME move data to db?
    return JsonResponse([
        {
            'title': 'Burger',
            'src': static('burger.jpg'),
            'text': 'Tasty Burger at your door step',
        },
        {
            'title': 'Spices',
            'src': static('food.jpg'),
            'text': 'All Cuisines',
        },
        {
            'title': 'New York',
            'src': static('tasty.jpg'),
            'text': 'Food is incomplete without a tasty dessert',
        }
    ], safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })


def product_list_api(request):
    products = Product.objects.select_related('category').available()

    dumped_products = []
    for product in products:
        dumped_product = {
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'special_status': product.special_status,
            'description': product.description,
            'category': {
                'id': product.category.id,
                'name': product.category.name,
            },
            'image': product.image.url,
            'restaurant': {
                'id': product.id,
                'name': product.name,
            }
        }
        dumped_products.append(dumped_product)
    return JsonResponse(dumped_products, safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })

@transaction.atomic
@api_view(['POST'])
def register_order(request):
    serializer = ProductSerialiser(data=request.data)
    serializer.is_valid(raise_exception=True)
    products_order = serializer.validated_data['products']

    create_order = FoodOrder.objects.create(
        firstname=serializer.validated_data['firstname'],
        lastname=serializer.validated_data['lastname'],
        phonenumber=serializer.validated_data['phonenumber'],
        address=serializer.validated_data['address']
    )

    FoodOrderProduct.objects.bulk_create(
        [
            FoodOrderProduct(order=create_order,
                             product=product['product'],
                             quantity=(product['quantity']),
                             price=Product.objects.get(
                                 name=product['product']).price)
            for product in products_order
        ]
    )

    allrestaurantmenu = RestaurantMenuItem.objects.select_related(
        'restaurant').select_related('product').all()
    all_restaurants = []
    suitable_restaurant = []
    all_order_in_one = False

    for product in products_order:
        need_restaurants = allrestaurantmenu.filter(
            product__name=product['product'])
        one_burger_restaurants = []
        for need_restaurant in need_restaurants:
            one_burger_restaurants.append(need_restaurant.restaurant.name)
        all_restaurants.append(one_burger_restaurants)

    if all_restaurants:
        first_burger_restaurants = all_restaurants[0]
        for first_burger_restaurant in first_burger_restaurants:
            for current_burger_restaurants in all_restaurants:
                if first_burger_restaurant not in current_burger_restaurants:
                    continue
            suitable_restaurant.append(first_burger_restaurant)

        for restaurant in suitable_restaurant:
            restuarant_object = get_object_or_404(Restaurant, name=restaurant)
            create_order.recommended_restaurants.add(restuarant_object)
        create_order.save()

    return Response(serializer.data, status=201)
