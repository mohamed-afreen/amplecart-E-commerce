# Generated by Django 4.1.3 on 2022-12-14 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_products', '0005_products_new_owner_products_old_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='old_owner',
            field=models.CharField(default='admin', max_length=100),
        ),
    ]
