# Generated by Django 4.1.3 on 2023-01-06 04:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0011_order_wallet_order_wallet_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='wallet_amount',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
    ]
