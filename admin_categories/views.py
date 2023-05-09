from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.views.decorators.cache import never_cache
from admin_products.models import *
from django.utils.datastructures import MultiValueDictKeyError


# Create your views here.

@never_cache
def category(request):
    if request.user.is_authenticated and request.user.is_superuser:
        category = Category.objects.all()
        return render(request, 'admin_category.html', {'category': category})
    else:
        return redirect('admin_login')


def add_category(request):
    if request.user.is_authenticated and request.user.is_superuser:
        if request.method == 'GET':
            return render(request, 'add_category.html')
        if request.method == 'POST':
            category_name = request.POST['category_name']

            if Category.objects.filter(category_name=category_name).exists():
                messages.error(request, 'Category Already Exists!')
                return redirect(add_category)

            category = Category.objects.create(category_name=category_name)
            category.save()
        return redirect('category')
    else:
        return redirect('admin_login')


def delete_category(request, id):
    if request.user.is_authenticated and request.user.is_superuser:
        category = Category.objects.get(id=id)
        category.delete()
        return redirect('category')
    return redirect('admin_login')
