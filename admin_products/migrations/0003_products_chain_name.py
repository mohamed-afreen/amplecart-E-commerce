# Generated by Django 4.1.3 on 2022-11-27 05:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_products', '0002_remove_category_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='chain_name',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
