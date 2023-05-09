# Generated by Django 4.1.3 on 2022-12-27 11:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cart', '0005_delete_balance'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ordered_date', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(default='Confirmed', max_length=100)),
                ('amount', models.FloatField(default=1)),
                ('method', models.CharField(default='Cash On Delivery', max_length=100)),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cart.address')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='oldcart',
            name='purchase',
        ),
        migrations.DeleteModel(
            name='purchase',
        ),
        migrations.AddField(
            model_name='oldcart',
            name='order',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='cart.order'),
        ),
    ]
