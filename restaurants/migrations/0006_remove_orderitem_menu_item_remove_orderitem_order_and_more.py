# Generated by Django 4.2.4 on 2025-03-20 11:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0005_order_paid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='menu_item',
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='order',
        ),
        migrations.DeleteModel(
            name='Order',
        ),
        migrations.DeleteModel(
            name='OrderItem',
        ),
    ]
