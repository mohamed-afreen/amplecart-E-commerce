# Generated by Django 4.1.3 on 2022-12-30 07:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('admin_products', '0008_products_is_active'),
        ('cart', '0009_alter_order_method'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='admin_products.products'),
        ),
    ]
