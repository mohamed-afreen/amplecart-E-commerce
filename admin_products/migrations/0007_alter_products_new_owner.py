# Generated by Django 4.1.3 on 2022-12-16 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_products', '0006_alter_products_old_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='new_owner',
            field=models.CharField(default='admin', max_length=100),
        ),
    ]
