# Generated by Django 3.2 on 2022-03-23 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0048_auto_20220323_1428'),
    ]

    operations = [
        migrations.AlterField(
            model_name='foodorder',
            name='payment_method',
            field=models.CharField(blank=True, choices=[('CASH', 'Наличными'), ('CARD', 'Картой')], max_length=10, verbose_name='Способ оплаты'),
        ),
    ]