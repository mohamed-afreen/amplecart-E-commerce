# Generated by Django 4.1.3 on 2022-12-29 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_products', '0007_alter_products_new_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]