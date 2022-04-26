from django import forms
from django.contrib.auth import authenticate, login
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from geopy import distance

from foodcartapp.models import Coordinate, FoodOrder, Product, Restaurant
from foodcartapp.yandex_adress_to_coordinate import get_object_coordinates


class Login(forms.Form):
    username = forms.CharField(
        label='Логин', max_length=75, required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Укажите имя пользователя'
        })
    )
    password = forms.CharField(
        label='Пароль', max_length=75, required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите пароль'
        })
    )


class LoginView(View):
    def get(self, request, *args, **kwargs):
        form = Login()
        return render(request, "login.html", context={
            'form': form
        })

    def post(self, request):
        form = Login(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                if user.is_staff:  # FIXME replace with specific permission
                    return redirect("restaurateur:RestaurantView")
                return redirect("start_page")

        return render(request, "login.html", context={
            'form': form,
            'ivalid': True,
        })


class LogoutView(auth_views.LogoutView):
    next_page = reverse_lazy('restaurateur:login')


def is_manager(user):
    return user.is_staff  # FIXME replace with specific permission


@user_passes_test(is_manager, login_url='restaurateur:login')
def view_products(request):
    restaurants = list(Restaurant.objects.order_by('name'))
    products = list(Product.objects.prefetch_related('menu_items'))

    default_availability = {restaurant.id: False for restaurant in restaurants}
    products_with_restaurants = []
    for product in products:

        availability = {
            **default_availability,
            **{item.restaurant_id: item.availability for item in product.menu_items.all()},
        }
        orderer_availability = [availability[restaurant.id] for restaurant in restaurants]

        products_with_restaurants.append(
            (product, orderer_availability)
        )

    return render(request, template_name="products_list.html", context={
        'products_with_restaurants': products_with_restaurants,
        'restaurants': restaurants,
    })


@user_passes_test(is_manager, login_url='restaurateur:login')
def view_restaurants(request):
    return render(request, template_name="restaurants_list.html", context={
        'restaurants': Restaurant.objects.all(),
    })


@user_passes_test(is_manager, login_url='restaurateur:login')
def view_orders(request):
    order_context = []
    order_details = FoodOrder.objects.all().prefetch_related(
        'food_order_products').get_orders_sums()
    orders_addresses = []
    for order in order_details:
        orders_addresses.append(order.address)

    orders_coordinates = Coordinate.objects.filter(
        address__in=orders_addresses)
    normalised_orders_coordinates = list(orders_coordinates.values('address', 'lon', 'lat'))
    all_restaurants = Restaurant.objects.select_related('coordinate').all()

    for restaurant in all_restaurants:
        if not restaurant.coordinate:
            restaurant_coordinate = get_object_coordinates(restaurant.address)
            restaurant.coordinate = restaurant_coordinate
            restaurant.coordinate.save()

    for order in order_details:
        in_base = False
        for normalised_order_coordinates in normalised_orders_coordinates:
            if order.address in normalised_order_coordinates['address']:
                order_coordinate = (
                    normalised_order_coordinates['lon'], normalised_order_coordinates['lat'])
                in_base = True
                continue
        if not in_base:
            order_coordinate = get_object_coordinates(order.address)
            if order_coordinate:
                order_coordinate = (
                    order_coordinate.lon, order_coordinate.lat)
            else: order_coordinate = None

        sorted_way_to_customer = {}
        way_to_customer = dict()
        for restaurant in order.recommended_restaurants.all():

            if order_coordinate:
                restaurant_coordinate = (
                    restaurant.coordinate.lat, restaurant.coordinate.lon)
                object_coordinate_lon, object_coordinate_lon = order_coordinate
                normal_orders_coordinate = (
                    object_coordinate_lon, object_coordinate_lon)
                order_to_restaurant_distance = distance.distance(
                    restaurant_coordinate, normal_orders_coordinate).km
                way_to_customer[restaurant.name] = order_to_restaurant_distance

            else:
                sorted_way_to_customer[restaurant.name] = 'не удалось расчитать расстояние'

        sorted_way_to_customer_keys = sorted(
            way_to_customer, key=way_to_customer.get)
        sorted_way_to_customer = {
            key: way_to_customer[key] for key in sorted_way_to_customer_keys
        }
        order_context.append(
        {
            "id": order.id,
            "order_status": order.get_order_status_display,
            "order_summ": order.order_summ,
            "firstname": order.firstname,
            "lastname": order.lastname,
            "phonenumber": order.phonenumber,
            "address": order.address,
            "comments": order.comments,
            "payment_method": order.get_payment_method_display,
            "recommended_restaurants": sorted_way_to_customer,}
    )
    context = {
        'order_items': order_context,
    }
    return render(request, template_name='order_items.html', context=context)
