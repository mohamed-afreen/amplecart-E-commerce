# Generated by Django 4.1.3 on 2023-01-06 04:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_wallet'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wallet',
            name='amount',
            field=models.DecimalField(blank=True, decimal_places=2, default=1000, max_digits=7, null=True),
        ),
    ]
