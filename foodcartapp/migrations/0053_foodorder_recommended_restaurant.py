# Generated by Django 3.2 on 2022-03-25 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0052_alter_foodorder_restaurant'),
    ]

    operations = [
        migrations.AddField(
            model_name='foodorder',
            name='recommended_restaurant',
            field=models.ManyToManyField(blank=True, related_name='orders', to='foodcartapp.Restaurant', verbose_name='Рекомендованые рестораны'),
        ),
    ]
