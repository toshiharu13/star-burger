# Generated by Django 3.2 on 2022-03-23 14:28

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0047_alter_foodorder_creation_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='foodorder',
            name='payment_method',
            field=models.CharField(blank=True, choices=[('CASH', 'Наличными'), ('CARD', 'Карстой')], max_length=10, verbose_name='Способ оплаты'),
        ),
        migrations.AlterField(
            model_name='foodorder',
            name='creation_date',
            field=models.DateTimeField(db_index=True, default=django.utils.timezone.now, null=True, verbose_name='Время создания заказа'),
        ),
        migrations.AlterField(
            model_name='foodorder',
            name='order_status',
            field=models.CharField(choices=[('NEW', 'Новый'), ('PROGRESS', 'В работе'), ('FINISHED', 'Закончен')], db_index=True, default='NEW', max_length=10, verbose_name='Статус заказа'),
        ),
    ]