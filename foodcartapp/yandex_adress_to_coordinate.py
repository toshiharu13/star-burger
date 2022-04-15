import django.conf
import requests

from foodcartapp.models import Coordinate


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


def get_object_coordinate(address):
    yandex_key = django.conf.settings.YANDEX_KEY
    coordinates = fetch_coordinates(yandex_key, address)
    if coordinates:
        rest_lon, rest_lat = coordinates
        restaurant_coordinate_oblect, created = Coordinate.objects.get_or_create(
            address=address,
            lon=rest_lon,
            lat=rest_lat, )
        return restaurant_coordinate_oblect






