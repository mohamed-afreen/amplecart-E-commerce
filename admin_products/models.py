from django.db import models

# Create your models here.


class Category(models.Model):

    category_name = models.CharField(max_length=50)

    def __str__(self):
        return self.category_name


class Products(models.Model):

    product_name = models.CharField(max_length=300)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.IntegerField(default=0)
    desc = models.CharField(max_length=1000)
    image = models.ImageField(
        upload_to="images", default="", null=True, blank=True)
    chain = models.CharField(max_length=100, blank=True)
    old_owner = models.CharField(
        max_length=100, default="afrinjasim", null=True)
    new_owner = models.CharField(
        max_length=100, default="afrinjasim", null=True)
    is_active = models.BooleanField(default=True)
    reselled = models.BooleanField(default="", null=True)

    def __str__(self):
        return self.product_name
