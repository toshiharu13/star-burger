from django.core.management.base import BaseCommand, CommandError
from foodcartapp.models import Restaurant

from foodcartapp.yandex_adress_to_coordinate import get_object_coordinate


class Command(BaseCommand):
    help = 'Fill addreses of restaurants'

    def add_arguments(self, parser):
        parser.add_argument(
            '-a',
            '--addressess',
            action='store_true',
            default=False,
            help='Fill addreses of restaurants',)

    def handle(self, *args, **options):
        if options['addressess']:
            all_restaurants = Restaurant.objects.select_related(
                'coordinate').all()

            for restaurant_object in all_restaurants:
                if not restaurant_object.coordinate:
                    coordinate_object = get_object_coordinate(
                        restaurant_object.address)
                    restaurant_object.coordinate = coordinate_object
                    restaurant_object.coordinate.save()
            print('done')

