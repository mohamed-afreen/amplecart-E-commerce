# Generated by Django 4.1.3 on 2022-12-27 12:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0007_remove_order_address'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='oldcart',
            name='quantity',
        ),
    ]
