from django.http import JsonResponse
from django.templatetags.static import static
import json
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response

from .models import Product, FoodOrderProduct, FoodOrder


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


@api_view(['POST'])
def register_order(request):
    #print(request.data)
    order = request.data
    try:
        products_order = order['products']
        if products_order == []:
            content = {'products: Этот список не может быть пустым.'}
            return Response(content, status.HTTP_406_NOT_ACCEPTABLE)
        # print(products_order)
        order = FoodOrder.objects.create(
            firstname=order['firstname'],
            lastname=order['lastname'],
            phone_number=order['phonenumber'],
            address=order['address']
        )

        FoodOrderProduct.objects.bulk_create(
            [
                FoodOrderProduct(order=order,
                                 product=Product.objects.get(
                                     id=int(product['product'])),
                                 quantity=int(product['quantity']),)
                for product in products_order
            ]
        )
    except TypeError:
        if type(products_order) == str:
            content = {'products: Ожидался list со значениями, но был получен "str".'}
            return Response(content, status=status.HTTP_406_NOT_ACCEPTABLE)
        elif not products_order:
            content = {'products: Это поле не может быть пустым.'}
            return Response(content, status.HTTP_406_NOT_ACCEPTABLE)

    except KeyError:
        content = {'products: Обязательное поле.'}
        return Response(content, status.HTTP_406_NOT_ACCEPTABLE)
    return JsonResponse({})
