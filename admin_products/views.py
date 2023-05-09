from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth import login, logout, authenticate
from django.views.decorators.cache import never_cache
from .models import *
from cart.models import *
from django.utils.datastructures import MultiValueDictKeyError


# Create your views here.


@never_cache
def admin_products(request):
    if request.user.is_authenticated and request.user.is_superuser:

        soldout_count = Products.objects.all()
        is_active = Products.objects.all()
        products = Products.objects.all()
        is_active = Products.objects.filter(is_active=True).count()
        soldout_count = Products.objects.filter(is_active=False).count()
        return render(request, 'token_list.html', {'products': products, 'is_active': is_active, 'soldout_count': soldout_count})
    else:
        return redirect('admin_login')


def add_product(request):
    if request.user.is_superuser:
        if request.method == 'GET':
            category = Category.objects.all()
            return render(request, 'add_token.html', {'category': category})

        if request.method == 'POST':
            product_name = request.POST['product_name']
            category = request.POST['category']
            price = request.POST['price']
            desc = request.POST['desc']
            chain = request.POST['chain']
            # new_owner = request.user

            try:
                image = request.FILES['image']
            except MultiValueDictKeyError:
                messages.info(request, 'Upload image')
                return redirect(add_product)

            category = Category.objects.get(id=category)
            product = Products.objects.create(
                product_name=product_name, desc=desc, price=price, category=category, image=image, chain=chain)
            product.save()
            return redirect(admin_products)
    return redirect('admin_login')


@never_cache
def edit_product(request, id):
    if request.user.is_superuser:
        product = Products.objects.get(id=id)

        if request.method == 'POST':

            product_name = request.POST['product_name']
            category = request.POST['category']
            price = request.POST['price']
            desc = request.POST['desc']
            image = request.FILES.get('image', product.image)
            chain = request.POST['chain']

            category = Category.objects.get(id=category)
            product.product_name = product_name
            product.category = category
            product.image = image
            product.price = price
            product.desc = desc
            product.chain = chain
            product.save()
            return redirect(admin_products)

        category = Category.objects.all()
        return render(request, 'edit_token.html', {'product': product, 'category': category})
    return redirect('admin_login')


def delete_product(request, id):
    if request.user.is_superuser:
        product = Products.objects.get(id=id)
        product.delete()
        return redirect(admin_products)
    return redirect('admin_login')


def soldout_products(request):
    if request.user.is_authenticated and request.user.is_superuser:

        orders = Order.objects.all()
        reselled_by = Order.objects.filter(user=request.user)
        products = Products.objects.all()
        soldout_count = Order.objects.all().count()
        return render(request, 'soldout_products.html', {'products': products, 'soldout_count': soldout_count, 'reselled_by': reselled_by, 'orders': orders})
    else:
        return redirect('admin_login')
