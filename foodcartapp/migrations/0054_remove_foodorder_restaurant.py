# Generated by Django 3.2 on 2022-03-25 12:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0053_foodorder_recommended_restaurant'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='foodorder',
            name='restaurant',
        ),
    ]
