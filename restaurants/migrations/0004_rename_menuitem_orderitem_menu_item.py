# Generated by Django 5.1.7 on 2025-03-19 20:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0003_orderitem'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderitem',
            old_name='menuitem',
            new_name='menu_item',
        ),
    ]
