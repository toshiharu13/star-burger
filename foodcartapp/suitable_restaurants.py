from .models import RestaurantMenuItem


def get_suitable_restaurants(order_products):
    all_restaurants_menu = RestaurantMenuItem.objects.select_related(
            'restaurant').select_related('product').all()
    splitted_suitable_restaurants = []
    suitable_restaurants = []

    for product in order_products:
        suitable_restaurants = all_restaurants_menu.filter(
            product__name=product['product'])
        sorted_by_product_restaurants = []
        for suitable_restaurants in suitable_restaurants:
            sorted_by_product_restaurants.append(suitable_restaurants.restaurant.name)
        splitted_suitable_restaurants.append(sorted_by_product_restaurants)

    if splitted_suitable_restaurants:
        first_burger_restaurants = splitted_suitable_restaurants[0]
        for first_burger_restaurant in first_burger_restaurants:
            for current_burger_restaurants in splitted_suitable_restaurants:
                if first_burger_restaurant not in current_burger_restaurants:
                    continue
            suitable_restaurants.append(first_burger_restaurant)

        return suitable_restaurants
