from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import F, Sum
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField


class FoodOrderQuerySet(models.QuerySet):
    def get_orders_sums(self):
        order_summ = self.annotate(order_summ=Sum(
            F('food_order_products__price') *
            F('food_order_products__quantity')))
        return order_summ

    def get_suitable_restaurants(self):
        normalized_restaurants_menu = list(RestaurantMenuItem.objects.filter(
            availability=True).select_related(
            'restaurant').select_related('product').all().values(
            'restaurant__name', 'product__name'))
        food_orders_products = FoodOrderProduct.objects.all().select_related(
            'order').select_related('product')
        splitted_suitable_restaurants = []
        suitable_restaurants_menu = set()

        for order_product in food_orders_products:
            for suitable_restaurant in normalized_restaurants_menu:
                if order_product.product.name == suitable_restaurant['product__name']:
                    suitable_restaurants_menu.add(
                        suitable_restaurant['restaurant__name'])
            suitable_restaurants = set()
            splitted_suitable_restaurants.append(suitable_restaurants_menu)

            if splitted_suitable_restaurants:
                template_burger_restaurants = splitted_suitable_restaurants[0]
                for template_burger_restaurant in template_burger_restaurants:
                    for current_burger_restaurants in splitted_suitable_restaurants:
                        if template_burger_restaurant not in current_burger_restaurants:
                            continue
                        suitable_restaurants.add(template_burger_restaurant)

            order_recommended_restaurants = self.get(
                pk=order_product.order.pk)
            if not order_recommended_restaurants.recommended_restaurants.all():
                for suitable_restaurant in suitable_restaurants:
                    try:
                        order_recommended_restaurants.recommended_restaurants.add(
                            Restaurant.objects.get(name=suitable_restaurant)
                        )
                    except ObjectDoesNotExist:
                        continue
                    except MultipleObjectsReturned:
                        continue
                order_recommended_restaurants.save()


class ProductQuerySet(models.QuerySet):
    def available(self):
        products = (
            RestaurantMenuItem.objects
            .filter(availability=True)
            .values_list('product')
        )
        return self.filter(pk__in=products)


class Coordinate(models.Model):
    address = models.CharField(max_length=50, blank=True)
    lon = models.FloatField('Долгота', null=True)
    lat = models.FloatField('Широта', null=True)

    class Meta:
        verbose_name = 'Координаты'
        verbose_name_plural = 'Координаты'

    def __str__(self):
        return f'{self.address}'


class Restaurant(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )
    address = models.CharField('адрес', max_length=100,)
    coordinate = models.ForeignKey(
        Coordinate,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Координаты')
    contact_phone = models.CharField(
        'контактный телефон',
        max_length=50,
        blank=True,)

    class Meta:
        verbose_name = 'ресторан'
        verbose_name_plural = 'рестораны'

    def __str__(self):
        return self.name


class ProductCategory(models.Model):
    name = models.CharField(
        'название',
        max_length=50)

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(
        'название',
        max_length=50)
    category = models.ForeignKey(
        ProductCategory,
        verbose_name='категория',
        related_name='products',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    price = models.DecimalField(
        'цена',
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)])
    image = models.ImageField('картинка')
    special_status = models.BooleanField(
        'спец.предложение',
        default=False,
        db_index=True,)
    description = models.TextField(
        'описание',
        max_length=250,
        blank=True,)
    objects = ProductQuerySet.as_manager()

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'

    def __str__(self):
        return self.name


class RestaurantMenuItem(models.Model):
    restaurant = models.ForeignKey(
        Restaurant,
        related_name='menu_items',
        verbose_name="ресторан",
        on_delete=models.CASCADE,)
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='menu_items',
        verbose_name='продукт',)
    availability = models.BooleanField(
        'в продаже',
        default=True,
        db_index=True)

    class Meta:
        verbose_name = 'пункт меню ресторана'
        verbose_name_plural = 'пункты меню ресторана'
        unique_together = [
            ['restaurant', 'product']
        ]

    def __str__(self):
        return f"{self.restaurant.name} - {self.product.name}"


class FoodOrder(models.Model):
    ORDER_STATUS = (
        ('NEW', 'Новый'),
        ('PROGRESS', 'В работе'),
        ('FINISHED', 'Закончен'),)
    PAYMENT_METHOD = (
        ('CASH', 'Наличными'),
        ('CARD', 'Картой'), )
    firstname = models.CharField('Имя', max_length=50)
    lastname = models.CharField('Фамилия', max_length=50, db_index=True)
    phonenumber = PhoneNumberField('Номер телефона', db_index=True)
    address = models.CharField('Адресс', max_length=100)
    order_status = models.CharField(
        'Статус заказа',
        max_length=10,
        choices=ORDER_STATUS,
        default='NEW',
        db_index=True)
    comments = models.TextField('Комментарии', blank=True)
    creation_date = models.DateTimeField(
        'Время создания заказа',
        default=timezone.now,
        db_index=True)
    call_time = models.DateTimeField('Когда позвонить', null=True, blank=True)
    delivery_time = models.DateTimeField(
        'Когда доставить',
        null=True,
        blank=True)
    payment_method = models.CharField(
        'Способ оплаты',
        max_length=10,
        choices=PAYMENT_METHOD,
        blank=True,
        db_index=True)
    recommended_restaurants = models.ManyToManyField(
        Restaurant,
        verbose_name='Рекомендованые рестораны',
        blank=True,
        related_name='food_orders')
    assigned_restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="orders",
        verbose_name='Назначеный ресторан')
    objects = FoodOrderQuerySet.as_manager()

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'{self.pk}-{self.firstname} {self.lastname} - {self.address}'


class FoodOrderProduct(models.Model):
    order = models.ForeignKey(FoodOrder,
                              on_delete=models.CASCADE,
                              related_name='food_order_products',
                              verbose_name='Заказ')
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE,
                                related_name='food_order_products',
                                verbose_name='Продукты заказа')
    quantity = models.PositiveIntegerField(
        'количество',
        validators=[MinValueValidator(1)])
    price = models.DecimalField(
        'цена',
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)])

    class Meta:
        verbose_name = 'Элементы заказа'
        verbose_name_plural = 'Элементы заказа'

    def __str__(self):
        return f'Из заказа {self.order.pk} - {self.product.name} '
