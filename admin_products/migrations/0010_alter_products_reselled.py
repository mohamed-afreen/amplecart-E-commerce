# Generated by Django 4.1.3 on 2023-01-09 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_products', '0009_products_reselled'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='reselled',
            field=models.BooleanField(default=None),
        ),
    ]