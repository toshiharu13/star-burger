# Generated by Django 3.2 on 2022-06-27 19:50

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Coordinate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(blank=True, max_length=50)),
                ('lon', models.FloatField(null=True, verbose_name='Долгота')),
                ('lat', models.FloatField(null=True, verbose_name='Широта')),
            ],
            options={
                'verbose_name': 'Координаты',
                'verbose_name_plural': 'Координаты',
            },
        ),
        migrations.CreateModel(
            name='FoodOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(max_length=50, verbose_name='Имя')),
                ('lastname', models.CharField(db_index=True, max_length=50, verbose_name='Фамилия')),
                ('phonenumber', phonenumber_field.modelfields.PhoneNumberField(db_index=True, max_length=128, region=None, verbose_name='Номер телефона')),
                ('address', models.CharField(max_length=100, verbose_name='Адрес')),
                ('order_status', models.CharField(choices=[('NEW', 'Новый'), ('PROGRESS', 'В работе'), ('FINISHED', 'Закончен')], db_index=True, default='NEW', max_length=10, verbose_name='Статус заказа')),
                ('comments', models.TextField(blank=True, verbose_name='Комментарии')),
                ('creation_date', models.DateTimeField(db_index=True, default=django.utils.timezone.now, verbose_name='Время создания заказа')),
                ('call_time', models.DateTimeField(blank=True, null=True, verbose_name='Когда позвонить')),
                ('delivery_time', models.DateTimeField(blank=True, null=True, verbose_name='Когда доставить')),
                ('payment_method', models.CharField(blank=True, choices=[('CASH', 'Наличными'), ('CARD', 'Картой')], db_index=True, max_length=10, verbose_name='Способ оплаты')),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Заказы',
            },
        ),
        migrations.CreateModel(
            name='ProductCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='название')),
            ],
            options={
                'verbose_name': 'категория',
                'verbose_name_plural': 'категории',
            },
        ),
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='название')),
                ('address', models.CharField(max_length=100, verbose_name='адрес')),
                ('contact_phone', models.CharField(blank=True, max_length=50, verbose_name='контактный телефон')),
                ('coordinate', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='foodcartapp.coordinate', verbose_name='Координаты')),
            ],
            options={
                'verbose_name': 'ресторан',
                'verbose_name_plural': 'рестораны',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='название')),
                ('price', models.DecimalField(decimal_places=2, max_digits=8, validators=[django.core.validators.MinValueValidator(0)], verbose_name='цена')),
                ('image', models.ImageField(upload_to='', verbose_name='картинка')),
                ('special_status', models.BooleanField(db_index=True, default=False, verbose_name='спец.предложение')),
                ('description', models.TextField(blank=True, max_length=250, verbose_name='описание')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='products', to='foodcartapp.productcategory', verbose_name='категория')),
            ],
            options={
                'verbose_name': 'товар',
                'verbose_name_plural': 'товары',
            },
        ),
        migrations.CreateModel(
            name='FoodOrderProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='количество')),
                ('price', models.DecimalField(decimal_places=2, max_digits=8, validators=[django.core.validators.MinValueValidator(0)], verbose_name='цена')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='food_order_products', to='foodcartapp.foodorder', verbose_name='Заказ')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='food_order_products', to='foodcartapp.product', verbose_name='Продукты заказа')),
            ],
            options={
                'verbose_name': 'Элементы заказа',
                'verbose_name_plural': 'Элементы заказа',
            },
        ),
        migrations.AddField(
            model_name='foodorder',
            name='assigned_restaurant',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='assigned_for_food_orders', to='foodcartapp.restaurant', verbose_name='Назначеный ресторан'),
        ),
        migrations.CreateModel(
            name='RestaurantMenuItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('availability', models.BooleanField(db_index=True, default=True, verbose_name='в продаже')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='menu_items', to='foodcartapp.product', verbose_name='продукт')),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='menu_items', to='foodcartapp.restaurant', verbose_name='ресторан')),
            ],
            options={
                'verbose_name': 'пункт меню ресторана',
                'verbose_name_plural': 'пункты меню ресторана',
                'unique_together': {('restaurant', 'product')},
            },
        ),
    ]
