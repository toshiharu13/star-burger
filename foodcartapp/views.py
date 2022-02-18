from django.http import JsonResponse
from django.templatetags.static import static
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response

from .models import Product, FoodOrderProduct, FoodOrder
from foodcartapp.serializers import ProductSerialiser


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
    serializer = ProductSerialiser(data=request.data)
    serializer.is_valid(raise_exception=True)
    order = request.data
    try:
        products_order = order['products']

        for product in products_order:
            if not Product.objects.filter(id__contains=product['product']):
                content = {
                    f'products: Недопустимый первичный ключ {product["product"]}'}
                return Response(content, status.HTTP_406_NOT_ACCEPTABLE)
        if (not order['firstname']
            and not order['lastname']
            and not order['phonenumber']
            and not order['address']
        ):
            content = {
                'firstname, lastname, phonenumber, address: Это поле не может быть пустым.'}
            return Response(content, status.HTTP_406_NOT_ACCEPTABLE)
        if products_order == []:
            content = {'products: Этот список не может быть пустым.'}
            return Response(content, status.HTTP_406_NOT_ACCEPTABLE)
        if not isinstance(order['firstname'], str):
            content = {'firstname: Not a valid string.'}
            return Response(content, status.HTTP_406_NOT_ACCEPTABLE)
        if not order['firstname']:
            content = {'firstname: Это поле не может быть пустым.'}
            return Response(content, status.HTTP_406_NOT_ACCEPTABLE)
        if not order['phonenumber']:
            content = {'phonenumber: Это поле не может быть пустым.'}
            return Response(content, status.HTTP_406_NOT_ACCEPTABLE)
        for digit in range(5):
            if order['phonenumber'][digit] == '0':
                content = {'phonenumber: Введен некорректный номер телефона'}
                return Response(content, status.HTTP_406_NOT_ACCEPTABLE)

        create_order = FoodOrder.objects.create(
            firstname=order['firstname'],
            lastname=order['lastname'],
            phonenumber=order['phonenumber'],
            address=order['address']
        )

        FoodOrderProduct.objects.bulk_create(
            [
                FoodOrderProduct(order=create_order,
                                 product=Product.objects.get(
                                     id=int(product['product'])),
                                 quantity=int(product['quantity']), )
                for product in products_order
            ]
        )
    except TypeError as error:
        if isinstance(products_order, str):
            content = {
                'products: Ожидался list со значениями, но был получен "str".'}
            return Response(content, status=status.HTTP_406_NOT_ACCEPTABLE)
        elif not products_order:
            content = {'products: Это поле не может быть пустым.'}
            return Response(content, status.HTTP_406_NOT_ACCEPTABLE)
        else:
            return Response(f'Ошибка - {error}', status.HTTP_400_BAD_REQUEST)

    except KeyError as error:
        if ('firstname' not in order
            and 'lastname' not in order
            and 'phonenumber' not in order
            and 'address' not in order
        ):
            content = {
                'firstname, lastname, phonenumber, address: Обязательное поле.'}
            return Response(content, status.HTTP_406_NOT_ACCEPTABLE)

        content = {'products: Обязательное поле.'}
        return Response(content, status.HTTP_406_NOT_ACCEPTABLE)

    return JsonResponse({})
