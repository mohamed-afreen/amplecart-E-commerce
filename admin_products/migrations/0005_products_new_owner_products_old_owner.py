# Generated by Django 4.1.3 on 2022-12-14 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_products', '0004_rename_chain_name_products_chain'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='new_owner',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='products',
            name='old_owner',
            field=models.CharField(default='', max_length=100),
        ),
    ]