# Generated by Django 4.1.3 on 2023-01-06 05:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_wallet_amount'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wallet',
            name='amount',
        ),
        migrations.AddField(
            model_name='wallet',
            name='wall_amount',
            field=models.FloatField(blank=True, default=1000, null=True),
        ),
    ]
