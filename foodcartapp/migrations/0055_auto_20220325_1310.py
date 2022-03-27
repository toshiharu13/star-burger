# Generated by Django 3.2 on 2022-03-25 13:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0054_remove_foodorder_restaurant'),
    ]

    operations = [
        migrations.CreateModel(
            name='Сoordinate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lon', models.FloatField(verbose_name='Долгота')),
                ('lat', models.FloatField(verbose_name='Широта')),
            ],
        ),
        migrations.AddField(
            model_name='restaurant',
            name='сoordinate',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='foodcartapp.сoordinate', verbose_name='Координаты'),
        ),
    ]