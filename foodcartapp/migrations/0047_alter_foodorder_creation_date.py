# Generated by Django 3.2 on 2022-03-23 14:12

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0046_auto_20220323_1409'),
    ]

    operations = [
        migrations.AlterField(
            model_name='foodorder',
            name='creation_date',
            field=models.DateTimeField(default=django.utils.timezone.now, null=True, verbose_name='Время создания заказа'),
        ),
    ]