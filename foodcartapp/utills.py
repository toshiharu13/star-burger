import requests
from environs import Env
from star_burger.wsgi import *

from foodcartapp.models import Restaurant, Coordinate


env = Env()
env.read_env()


def fetch_coordinates(apikey, address):
    base_url = "https://geocode-maps.yandex.ru/1.x"
    response = requests.get(base_url, params={
        "geocode": address,
        "apikey": apikey,
        "format": "json",
    })
    response.raise_for_status()
    found_places = response.json()['response']['GeoObjectCollection']['featureMember']

    if not found_places:
        return None

    most_relevant = found_places[0]
    lon, lat = most_relevant['GeoObject']['Point']['pos'].split(" ")
    return lon, lat


if __name__ == '__main__':


    all_restaurants = Restaurant.objects.select_related('coordinate').all()
    for restaurant in all_restaurants:
        if not restaurant.coordinate:
            rest_lon, rest_lat = fetch_coordinates(env.str('YANDEX_KEY'),
                                    restaurant.address)
            if not rest_lon and not rest_lat:
                continue
            restaurant_coordinate_oblect, created = Coordinate.objects.get_or_create(
                address=restaurant.address,
                lon=rest_lon,
                lat=rest_lat,)
            restaurant.coordinate = restaurant_coordinate_oblect
            restaurant.save()


