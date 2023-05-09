from django.db import models
from django.contrib.auth import get_user_model
from admin_products.models import *

User = get_user_model()

# Create your models here.


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    cancel = models.BooleanField(default=False)

    def __str__(self):
        return self.product


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    username = models.CharField(max_length=100)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, null=True, on_delete=models.CASCADE)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=100, default='Confirmed')
    amount = models.FloatField(default=1)
    method = models.CharField(max_length=100, default='paypal')
    wallet = models.BooleanField(default=False)
    wallet_amount = models.FloatField(default=0, null=True, blank=True)
    soldout = models.BooleanField(default=False)


class OldCart(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    cancel = models.BooleanField(default=False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, default=0)
    total = models.IntegerField(default=1)


class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    is_watchlist = models.BooleanField(default=True)


class guestCart(models.Model):
    quantity = models.IntegerField(default=1)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    user_ref = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.product.product_name


class productOffer(models.Model):
    product = models.ForeignKey(
        Products, on_delete=models.CASCADE, null=True, blank=True)
    offer = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)
