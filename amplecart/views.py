from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from admin_products.models import *
from cart.models import *
from django.db.models import Q


# Create your views here.


def home(request):

    categori = Category.objects.all()
    if 'search' in request.GET:
        search = request.GET['search']
        multiple_search = Q(Q(product_name__icontains=search)
                            | Q(chain__icontains=search))
        product = Products.objects.filter(multiple_search)
    else:
        product = Products.objects.all()
        categori = Category.objects.all()
    return render(request, "index.html", {'products': product, 'category': categori})


def defi_the_game(request):
    return render(request, "defi_the_game.html")


def art_blocks(request):
    return render(request, "art_blocks.html")


def blogs(request):
    return render(request, "blogs.html")
